from typing import Dict, List, Mapping, Tuple, Union

import torch
from torch import nn

from aixd.mlmodel.architecture.blocks import ResBlockFC
from aixd.mlmodel.architecture.heads import InHead, OutHead


class Encoder(nn.Module):
    """
    Encoder module of a conditional variational autoencoder.

    Parameters
    ----------
    in_heads : Dict[str, nn.Module]
        Dictionary of input heads, where the keys are strings and the values are PyTorch modules.
    out_heads : Dict[str, nn.Module]
        Dictionary of output heads, where the keys are strings and the values are PyTorch modules.
    splits : Dict[str, Tuple[int, int]]
        Start and end indices for each feature in the input data vectors.
    layer_widths : List[int]
        List of integer values representing the widths of the hidden layers in the encoder.
    latent_dim : int
        Integer value representing the latent dimension of the model.
    activation : str
        String representing the activation function to be used in the hidden layers of the encoder.
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

        in_channels = sum([head.out_channels for head in in_heads.values()])
        self.channels = [in_channels] + layer_widths
        self.blocks = [ResBlockFC(c, c_next, activation=activation) for c, c_next in zip(self.channels[:-1], self.channels[1:])]
        self.seq_blocks = nn.Sequential(*self.blocks)
        self.fc_z = nn.Linear(self.channels[-1], latent_dim)

    def forward(self, x) -> Dict[str, torch.Tensor]:
        """
        Forward pass of the encoder.

        Parameters
        ----------
        x : Dict[str, torch.Tensor]
            Dictionary of input tensors, where the keys are strings and the values are PyTorch tensors.

        Returns
        -------
        Dict[str, torch.Tensor]
            Dictionary of output tensors, where the keys are strings and the values are PyTorch tensors.
        """
        emb = torch.cat([head(x[:, self.splits[name][0] : self.splits[name][1]]) for name, head in self.in_heads.items()], dim=-1)
        lat = self.seq_blocks(emb)
        z = self.fc_z(lat)
        y = torch.cat([head(lat) for head in self.out_heads.values()], dim=-1)
        return {"z": z, "y": y}

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


class VEncoder(Encoder):
    """
    Encoder module of a conditional variational autoencoder with additional parameters for the latent distribution.

    Parameters
    ----------
    in_heads : Dict[str, nn.Module]
        Dictionary of input heads, where the keys are strings and the values are PyTorch modules.
    out_heads : Dict[str, nn.Module]
        Dictionary of output heads, where the keys are strings and the values are PyTorch modules.
    splits : Dict[str, Tuple[int, int]]
        Start and end indices for each feature in the input data vectors.
    layer_widths : List[int]
        List of integer values representing the widths of the hidden layers in the encoder.
    latent_dim : int
        Integer value representing the latent dimension of the model.
    activation : str
        String representing the activation function to be used in the hidden layers of the encoder.
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
        super().__init__(in_heads, out_heads, splits, layer_widths, latent_dim, activation)
        self.fc_z_log_var = nn.Linear(self.channels[-1], latent_dim)

    def forward(self, x) -> Dict[str, torch.Tensor]:
        """
        Forward pass of the encoder.

        Parameters
        ----------
        x : Dict[str, torch.Tensor]
            Dictionary of input tensors, where the keys are strings and the values are PyTorch tensors.

        Returns
        -------
        Dict[str, torch.Tensor]
            Dictionary of output tensors, where the keys are strings and the values are PyTorch tensors.
        """
        emb = torch.cat([head(x[:, self.splits[name][0] : self.splits[name][1]]) for name, head in self.in_heads.items()], dim=-1)
        lat = self.seq_blocks(emb)
        z_mean, z_log_var = self.fc_z(lat), self.fc_z_log_var(lat)
        z = torch.distributions.Normal(z_mean, torch.exp(z_log_var / 2)).rsample()
        y = torch.cat([head(lat) for head in self.out_heads.values()], dim=-1)
        return {"z": z, "y": y, "z_mean": z_mean, "z_log_var": z_log_var}
