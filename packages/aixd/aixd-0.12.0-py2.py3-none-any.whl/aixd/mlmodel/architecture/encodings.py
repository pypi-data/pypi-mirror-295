import torch
from torch import nn
from torch.nn import functional as F


class OneHotEncoding(nn.Module):
    """
    A one hot encoding layer. This layer takes a tensor of shape (batch_size, 1) and returns a one-hot encoded tensor.

    Parameters
    ----------
    num_classes : int
        The number of classes for the one-hot encoding.
    """

    def __init__(self, num_classes: int):
        super().__init__()
        if num_classes <= 2:
            raise ValueError(f"Expected num_classes to be greater than 2, but got {num_classes}")

        self.num_classes = num_classes

    def forward(self, x: torch.Tensor):
        if x.ndim == 1:
            x = x.unsqueeze(1)

        if x.shape != (x.shape[0], 1):
            raise ValueError(f"Expected input shape to be (batch_size, 1), but got {x.shape}")

        return F.one_hot(x.squeeze(1).long(), num_classes=self.num_classes)  # out shape: (batch_size, num_classes)
