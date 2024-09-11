import torch
import torch.nn as nn


class CrossEntropyLoss(nn.CrossEntropyLoss):
    """
    Same as nn.CrossEntropyLoss, but with the option to pass the target as class indices with custom dimension handling.

    Parameters
    ----------
    class_indices : bool, optional, default=False
        Whether the target is passed as class indices.
    **kwargs
        Additional keyword arguments to be passed to nn.CrossEntropyLoss.
    """

    def __init__(self, class_indices: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.class_indices = class_indices

    def forward(self, input: torch.Tensor, target: torch.Tensor):
        if self.class_indices:
            # Check sizes
            if target.ndim > 2:
                raise ValueError(f"Expected target to have at most 2 dimensions, but got {target.ndim}")

            # Convert target to int and squeeze if necessary
            target = target.long()
            target = target.squeeze() if target.ndim == 2 else target

        return super().forward(input, target)


class LossStd(nn.Module):
    """
    Loss for the standard deviation of the values. It penalizes them
    deviating from a zero mean and a unit standard deviation.
    """

    def __init__(self):
        super().__init__()

    def forward(self, x):
        loss = torch.mean((1 - torch.std(x, dim=0)) ** 2)
        loss += torch.mean((torch.mean(x, dim=0)) ** 2)
        return loss


class MGEloss(nn.Module):
    """
    Mean gradient error. Uses a sobel filter to compute the gradient of predicted
    and estimated images, and then applies a mean square difference of the pixel-wise
    gradients.
    """

    def __init__(self):
        super().__init__()
        self.filter = nn.Conv2d(in_channels=1, out_channels=2, kernel_size=3, stride=1, padding=0, bias=False)
        Gx = torch.tensor([[2.0, 0.0, -2.0], [4.0, 0.0, -4.0], [2.0, 0.0, -2.0]])
        Gy = torch.tensor([[2.0, 4.0, 2.0], [0.0, 0.0, 0.0], [-2.0, -4.0, -2.0]])
        G = torch.cat([Gx.unsqueeze(0), Gy.unsqueeze(0)], 0)
        G = G.unsqueeze(1)
        self.filter.weight = nn.Parameter(G, requires_grad=False)

    def _compute_filter(self, img):
        """Auxiliary function to compute the gradient of an image"""
        x = self.filter(img)
        x = torch.mul(x, x)
        x = torch.sum(x, dim=1, keepdim=True)
        x = torch.sqrt(x + 1e-16)
        return x

    def forward(self, w_in, w_out, loss):
        gradient_in = self._compute_filter(w_in)
        gradient_out = self._compute_filter(w_out)
        return loss(gradient_out, gradient_in)
