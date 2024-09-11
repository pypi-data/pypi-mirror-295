from typing import Dict, List, Mapping, Tuple, Union

import torch
from torch import nn

from aixd.mlmodel.architecture.blocks import ResBlockFC
from aixd.mlmodel.architecture.heads import InHead, OutHead


class Decoder(nn.Module):
    """
    Decoder module of the conditional (variational) autoencoder.

    Parameters
    ----------
    in_heads : Dict[str, nn.Module]
        Dictionary of input heads, where the keys are strings and the values are PyTorch modules.
    out_heads : Dict[str, nn.Module]
        Dictionary of output heads, where the keys are strings and the values are PyTorch modules.
    layer_widths : List[int]
        List of integer values representing the widths of the hidden layers in the decoder.
    latent_dim : int
        Integer value representing the latent dimension of the model.
    activation : Union[nn.Module, str]
        nn.Module or string representing the activation function to be used in the hidden layers of the decoder.
    """

    def __init__(
        self,
        in_heads: Dict[str, InHead],
        out_heads: Dict[str, OutHead],
        splits: Dict[str, Tuple[int, int]],
        layer_widths: List[int],
        latent_dim: int,
        activation: Union[nn.Module, str],
    ):
        super().__init__()
        self.in_heads: Mapping[str, InHead] = nn.ModuleDict(in_heads)  # Use a ModuleDict and force the typing via Mapping (currently ModuleDict does not allow generic types)
        self.out_heads: Mapping[str, OutHead] = nn.ModuleDict(out_heads)  # Use a ModuleDict and force the typing via Mapping (currently ModuleDict does not allow generic types)
        self.splits = splits

        self.y_block = ResBlockFC(sum([head.out_channels for head in in_heads.values()]), layer_widths[0], activation=activation)
        self.z_block = ResBlockFC(latent_dim, layer_widths[0], activation=activation)
        self.channels = layer_widths
        self.blocks = [ResBlockFC(c, c_next, activation=activation) for c, c_next in zip(self.channels[:-1], self.channels[1:])]
        self.seq_blocks = nn.Sequential(*self.blocks)

    def forward(self, inputs: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Forward pass of the decoder.

        Parameters
        ----------
        inputs : Dict[str, torch.Tensor]
            Dictionary of input tensors, where the keys are strings and the values are PyTorch tensors.

        Returns
        -------
        Dict[str, torch.Tensor]
            Dictionary of output tensors, where the keys are strings and the values are PyTorch tensors.
        """
        z, y = inputs["z"], inputs["y"]
        emb_z = self.z_block(z)
        emb_y = self.y_block(torch.cat([head(y[:, self.splits[name][0] : self.splits[name][1]]) for name, head in self.in_heads.items()], dim=-1))
        lat = self.seq_blocks(emb_z + emb_y)
        return {"x": torch.cat([head(lat) for head in self.out_heads.values()], dim=-1)}

    def summary(self, detail: int = 1, flag_print: bool = True) -> Union[None, str]:
        """
        Prints a summary of a PyTorch model, including the number of parameters, the layers, their names, and the dimensionality.

        Parameters
        ----------
        detail : int, optional, default=1
            Controls the level of detail in the summary. Set to 1 to print the name and dimensionality of each layer.
        flag_print : bool, optional, default=True
            If `flag_print` is True, prints the summary. Otherwise, returns a string containing the summary.

        Returns
        -------
        Union[None, str]
            If `flag_print` is True, prints the summary. Otherwise, returns a string containing the summary.
        """
        total_params = sum(p.numel() for p in self.parameters())
        str_print = f"    Number of parameters: {total_params}"
        str_print += "\n    Layers:"
        for name, layer in self.named_children():
            str_print += f"\n      {name}: {layer.__class__.__name__}"
            if detail > 0:
                for param_name, param in layer.named_parameters():
                    str_print += f"\n        {param_name}: {param.shape}"

        if flag_print:
            print(str_print)
        else:
            return str_print
