from __future__ import annotations

from typing import List, Tuple, Union

import torch
from torch import nn

from aixd.mlmodel.architecture.blocks import CONV_2_PADDING, Activation, ResBlock1D, ResBlock2D, ResBlock3D, ResBlockFC, SelfAttn1D, SelfAttn2D, SelfAttn3D
from aixd.mlmodel.architecture.encodings import OneHotEncoding
from aixd.mlmodel.architecture.postprocessors import LogitsPostprocessor, PostprocessorMixIn, SigmoidPostprocessor, SoftmaxPostprocessor

SCALING_FACTOR = 2
INIT_CHANNELS = 8
MIN_SPATIAL_DIM = 3
MIN_PROD_SPATIAL_DIM = 64
DIM_CLASSES = {
    1: (ResBlock1D, SelfAttn1D, nn.Conv1d),
    2: (ResBlock2D, SelfAttn2D, nn.Conv2d),
    3: (ResBlock3D, SelfAttn3D, nn.Conv3d),
}


class Head(nn.Module):
    """Base class for all heads."""

    @property
    def in_channels(self) -> int:
        """The number of input channels."""
        raise NotImplementedError("Head subclasses must implement the in_channels property.")

    @property
    def out_channels(self) -> int:
        """The number of output channels."""
        raise NotImplementedError("Head subclasses must implement the out_channels property.")


class InHead(Head):
    """Abstract base class for all input heads."""

    def forward(self, x):
        raise NotImplementedError("InHead subclasses must implement the forward method.")


class OutHead(Head, PostprocessorMixIn):
    """Abstract base class for all output heads."""

    def forward(self, x):
        raise NotImplementedError("OutHead subclasses must implement the forward method.")


class InHeadFC(InHead):
    """
    Fully-Connected Feed-Forward Network for encoding an unstrucured, 1D feature.

    Parameters
    ----------
    in_channels : int
        The number of input channels.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str])
        The activation function to use.
    """

    def __init__(self, in_channels: int, latent_dims: List[int], activation: Union[nn.Module, str]):
        super().__init__()
        self.channels = [in_channels] + latent_dims
        self.blocks = [ResBlockFC(c, c_next, activation=activation) for c, c_next in zip(self.channels[:-1], self.channels[1:])]
        self.seq_blocks = nn.Sequential(*self.blocks)

    def forward(self, x):
        return self.seq_blocks(x)

    @property
    def out_channels(self) -> int:
        return self.channels[-1]

    @property
    def in_channels(self) -> int:
        return self.channels[0]


class OutHeadFC(OutHead):
    """
    Fully-Connected Feed-Forward Network for decoding an unstrucured, 1D feature.

    Parameters
    ----------
    in_channels : int
        The number of input channels.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    out_activation : Union[nn.Module, str], optional, default=None
        The activation function to use in the last layer.
    """

    def __init__(self, in_channels: int, latent_dims: List[int], activation: Union[nn.Module, str], out_activation: Union[nn.Module, str] = None):
        super().__init__()
        self.channels = [in_channels] + latent_dims
        self.blocks = [ResBlockFC(c, c_next, activation=activation) for c, c_next in zip(self.channels[:-2], self.channels[1:-1])]
        self.seq_blocks = nn.Sequential(*self.blocks)
        self.out_block = ResBlockFC(self.channels[-2], self.channels[-1], out_activation, dropout=False, batchnorm=False, residual=False)

    def forward(self, x):
        return self.out_block(self.seq_blocks(x))

    @property
    def out_channels(self) -> int:
        return self.channels[-1]

    @property
    def in_channels(self) -> int:
        return self.channels[0]


class InHeadConv(InHead):
    """
    Convolutional Network for encoding spatially strucured data in 1, 2 or 3 dimensions.

    Parameters
    ----------
    dim : int
        The dimensionality of the data: 1, 2 or 3.
    in_shape : Tuple[int]
        The shape of the input data.
    latent_dims : List[int])
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    attn_block_indices : List[int]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(self, dim: int, in_shape: Tuple[int], latent_dims: List[int], activation: Union[nn.Module, str], attn_block_indices: List[int]):
        super().__init__()
        self.dim = dim
        self.in_shape = in_shape
        self.res_block_class, self.attn_block_class, _ = DIM_CLASSES[self.dim]

        self.attn_block_indices = attn_block_indices

        self.channels = [in_shape[-1]] + latent_dims
        self.blocks = [
            (
                self.res_block_class(c, c_next, scaling="down", activation=activation)
                if i not in self.attn_block_indices
                else nn.Sequential(self.attn_block_class(c), self.res_block_class(c, c_next, scaling="down", activation=activation))
            )
            for i, (c, c_next) in enumerate(zip(self.channels[:-1], self.channels[1:]))
        ]
        self.seq_blocks = nn.Sequential(*self.blocks)
        self.global_pool = leaky_global_pool()

    def _auto_generate_latent_dims(self):
        """
        If no depth and widths of the CNN head are provided, this method adds layers with increasing width
        by multiplicative factor of 2 until either the product of all spatial dimensions is below
        MIN_PROD_SPATIAL_DIM, or the smallest dimension falls below MIN_SPATIAL_DIM.
        """
        channels = 8
        latent_dims = [channels]
        spatial_dims = list(self.in_shape[:-1])

        while torch.prod(torch.Tensor(spatial_dims)) >= MIN_PROD_SPATIAL_DIM and torch.Tensor(spatial_dims).min() >= MIN_SPATIAL_DIM:
            channels *= 2
            latent_dims.append(channels)
            spatial_dims = [d // 2 for d in spatial_dims]

        return latent_dims

    def forward(self, x):
        x = torch.reshape(x, (-1, *self.in_shape)).transpose(1, -1)
        return self.global_pool(self.seq_blocks(x))


class OutHeadConv(OutHead):
    """
    Convolutional Network for decoding spatially strucured data in 1, 2 or 3 dimensions.

    Parameters
    ----------
    dim : int
        The dimensionality of the data: 1, 2 or 3.
    in_shape : Tuple[int]
        The shape of the input data.
    target_shape : Tuple[int]
        Final shape that the output data should have.
    latent_dims : List[int])
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    out_activation : Union[nn.Module, str]
        The activation function to use in the last layer.
    attn_block_indices : List[int]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(
        self,
        dim: int,
        in_channels: int,
        target_shape: Tuple[int],
        latent_dims: List[int],
        activation: Union[nn.Module, str],
        out_activation: Union[nn.Module, str],
        attn_block_indices: List[int],
    ):
        super().__init__()
        self.dim = dim
        self.res_block_class, self.attn_block_class, self.conv_class = DIM_CLASSES[self.dim]
        self.attn_block_indices = attn_block_indices

        self.channels = latent_dims[:1] + latent_dims + [target_shape[-1]]
        self.paddings, self.latent_shape = self._get_paddings(target_shape, latent_dims)
        self.blocks = [
            (
                self.res_block_class(c, c_next, scaling="up", activation=activation, up_padding=p)
                if i not in self.attn_block_indices
                else nn.Sequential(self.attn_block_class(c), self.res_block_class(c, c_next, scaling="up", activation=activation, up_padding=p))
            )
            for i, (c, c_next, p) in enumerate(zip(self.channels[:-2], self.channels[1:-1], self.paddings))
        ]
        self.seq_blocks = nn.Sequential(*self.blocks)
        self.out_conv = self.conv_class(self.channels[-2], self.channels[-1], kernel_size=1)
        self.out_af = Activation(out_activation)
        self.reshape_layer = self._create_reshape_layer(in_channels, self.latent_shape)

    def _get_paddings(self, target_shape: Tuple[int], latent_dims: List[int]) -> List[List[int]]:
        """
        When performing downsampling on data with odd spatial dimensionality, the shape is divided by two and rounded down.
        Given the shape that the data should have after decoding, as well as the the number of layers in the head,
        this function determines, by how much each intermediate result must be cropped (negatively padded) to result
        in the original dimensionality.
        """
        paddings = []
        shape = target_shape[:-1]
        for _ in range(len(latent_dims)):
            paddings.append([CONV_2_PADDING if i % 2 == 0 or shape[i // 2] % 2 == 0 else CONV_2_PADDING - 1 for i in range(len(shape) * 2)])
            shape = [(s // 2) if s % 2 == 0 else (s // 2) + 1 for s in shape]
        return paddings[::-1], latent_dims[:1] + shape

    def _create_reshape_layer(self, in_channels: int, latent_shape: List[int]):
        """
        This method reshapes a one-dimensional vector into a shape that can be processed by this CNN head.
        If the vector does not have the right dimensionality to be directly reshaped, it is first passed
        through a linear layer.
        """
        if in_channels == torch.tensor(latent_shape).prod():
            return nn.Sequential(nn.Unflatten(1, latent_shape))
        else:
            return nn.Sequential(nn.Linear(in_channels, torch.tensor(latent_shape).prod()), nn.Unflatten(1, latent_shape))

    def _auto_generate_latent_dims(self):
        """
        If no depth and widths of the CNN head are provided, this method adds layers with increasing width
        by multiplicative factor of 2 until either the product of all spatial dimensions is below
        MIN_PROD_SPATIAL_DIM, or the smallest dimension falls below MIN_SPATIAL_DIM.
        """
        channels = INIT_CHANNELS
        latent_dims = [channels]
        spatial_dims = list(self.target_shape[:-1])

        while torch.prod(torch.Tensor(spatial_dims)) >= MIN_PROD_SPATIAL_DIM and torch.Tensor(spatial_dims).min() >= MIN_SPATIAL_DIM:
            channels *= 2
            latent_dims.append(channels)
            spatial_dims = [d // 2 for d in spatial_dims]

        return latent_dims[::-1]

    def forward(self, zy):
        h = self.reshape_layer(zy)
        h = self.seq_blocks(h)
        xh = self.out_af(self.out_conv(h).transpose(1, -1))
        return torch.reshape(xh, (xh.shape[0], -1))


class InHeadConv1D(InHeadConv):
    """
    Convolutional Network for encoding spatially strucured (temporal) data in 1 dimension.

    Parameters
    ----------
    in_shape : int
        The shape of the input data.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(self, in_shape: Tuple[int], latent_dims: List[int], activation: Union[nn.Module, str], attn_block_indices: List[int] = []):
        super().__init__(1, in_shape, latent_dims, activation, attn_block_indices)


class OutHeadConv1D(OutHeadConv):
    """
    Convolutional Network for decoding spatially strucured (temporal) data in 1 dimension.

    Parameters
    ----------
    in_channels : int
        The number of input channels.
    target_shape : Tuple[int]
        Final shape that the output data should have.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    out_activation : Union[nn.Module, str]
        The activation function to use in the last layer.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(
        self,
        in_channels: int,
        target_shape: Tuple[int],
        latent_dims: List[int],
        activation: Union[nn.Module, str],
        out_activation: Union[nn.Module, str] = None,
        attn_block_indices: List[int] = [],
    ):
        super().__init__(1, in_channels, target_shape, latent_dims, activation, out_activation, attn_block_indices)


class InHeadConv2D(InHeadConv):
    """
    Convolutional Network for encoding spatially strucured (image-like) data in 2 dimensions.

    Parameters
    ----------
    in_shape : int
        The shape of the input data.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(self, in_shape: Tuple[int], latent_dims: List[int], activation: Union[nn.Module, str], attn_block_indices: List[int] = []):
        super().__init__(2, in_shape, latent_dims, activation, attn_block_indices)


class OutHeadConv2D(OutHeadConv):
    """
    Convolutional Network for decoding spatially strucured (image-like) data in 2 dimensions.

    Parameters
    ----------
    in_channels : int
        The number of input channels.
    target_shape : Tuple[int]
        Final shape that the output data should have.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    out_activation : Union[nn.Module, str]
        The activation function to use in the last layer.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(
        self,
        in_channels: int,
        target_shape: Tuple[int],
        latent_dims: List[int],
        activation: Union[nn.Module, str],
        out_activation: Union[nn.Module, str] = None,
        attn_block_indices: List[int] = [],
    ):
        super().__init__(2, in_channels, target_shape, latent_dims, activation, out_activation, attn_block_indices)


class InHeadConv3D(InHeadConv):
    """
    Convolutional Network for encoding spatially strucured (MRI- or video-like) data in 3 dimensions.

    Parameters
    ----------
    in_shape : int
        The shape of the input data.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(self, in_shape: Tuple[int], latent_dims: List[int], activation: Union[nn.Module, str], attn_block_indices: List[int] = []):
        super().__init__(3, in_shape, latent_dims, activation, attn_block_indices)


class OutHeadConv3D(OutHeadConv):
    """
    Convolutional Network for decoding spatially strucured (MRI- or video-like) data in 3 dimensions.

    Parameters
    ----------
    in_channels : int
        The number of input channels.
    target_shape : Tuple[int]
        Final shape that the output data should have.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use.
    out_activation : Union[nn.Module, str]
        The activation function to use in the last layer.
    attn_block_indices : List[int], optional, default=[]
        Sequence of indices where to insert an attention layer in the encoding blocks.
    """

    def __init__(
        self,
        in_channels: int,
        target_shape: Tuple[int],
        latent_dims: List[int],
        activation: Union[nn.Module, str],
        out_activation: Union[nn.Module, str] = None,
        attn_block_indices: List[int] = [],
    ):
        super().__init__(3, in_channels, target_shape, latent_dims, activation, out_activation, attn_block_indices)


def leaky_global_pool(alpha: float = 0.1):
    """
    A function that performs a global pooling operation on the input tensor,
    combining the maximum and average (multiplied by a scaling factor) of all the spatial dimensions.
    Inspired by leaky relu activation supposed to improve the gradient flow.

    Parameters
    ----------
    x : torch.Tensor
        The input tensor.
    alpha : float, optional, default=0.1
        The weight given to the average value.
    """
    # TODO: maisseal, We should create a class for this, or use a general lambda layer
    return lambda x: (1 - alpha) * x.amax(dim=list(range(2, 2 + len(x.shape[2:])))) + alpha * x.mean(dim=list(range(2, 2 + len(x.shape[2:]))))


class CategoricalInHead(InHeadFC):
    """
    Fully-Connected Feed-Forward Network for encoding a categorical feature.

    Parameters
    ----------
    num_classes : int
        The number of classes.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use in the latent layers.
    """

    def __init__(self, num_classes: int, latent_dims: List[int], activation: Union[nn.Module, str]):
        self.num_classes = num_classes
        super().__init__(1 if self.is_binary() else self.num_classes, latent_dims, activation)

        # Modules can only be assigned after super().__init__ is called
        self.encoding = OneHotEncoding(num_classes) if not self.is_binary() else nn.Identity()

    def forward(self, x):
        x_encoded = self.encoding(x)
        return super().forward(x_encoded)

    def is_binary(self):
        """Returns True for binary classification tasks."""
        return self.num_classes == 2

    @property
    def in_channels(self) -> int:
        return 1

    @property
    def out_channels(self):
        return 1 if self.is_binary() else self.num_classes


class CategoricalOutHead(OutHeadFC):
    """
    Fully-Connected Feed-Forward Network for decoding a categorical feature. Sets the corresponding postprocessors based on the number of classes and the output activation.

    Parameters
    ----------
    num_classes : int
        The number of classes.
    in_channels : int
        The number of input channels.
    latent_dims : List[int]
        A list of integers representing the dimensions of the latent space. The length
        of the sequence defines the number of layers.
    activation : Union[nn.Module, str]
        The activation function to use in the latent layers.
    out_activation : Union[nn.Module, str], optional, default=None
        The activation function to use in the last layer. Either 'softmax' or 'sigmoid' for binary classification. If None, the output is assumed to be logits.
    """

    def __init__(self, num_classes: int, in_channels: int, latent_dims: List[int], activation: Union[nn.Module, str], out_activation: Union[nn.Module, str] = None):
        self.num_classes = num_classes
        self.out_activation = out_activation
        num_classes, latent_dims, out_activation = self._check_args(num_classes, latent_dims, out_activation)
        super().__init__(in_channels, latent_dims, activation, out_activation)

    def is_binary(self):
        """Returns True for binary classification tasks."""
        return self.num_classes == 2

    def _check_args(self, num_classes: int, latent_dims: List[int], out_activation: Union[nn.Module, str] = None):
        if self.is_binary():
            if not (out_activation is None or out_activation == "sigmoid" or isinstance(out_activation, nn.Sigmoid)):
                raise ValueError("For binary classification, the output activation must be 'sigmoid' or None.")
        else:
            if not (out_activation is None or out_activation == "softmax" or isinstance(out_activation, nn.Softmax)):
                raise ValueError("For multiclass classification, the output activation must be 'softmax' or None.")

        last_dim = 1 if self.is_binary() else num_classes
        if len(latent_dims) == 0 or latent_dims[-1] != last_dim:
            latent_dims.append(last_dim)

        return num_classes, latent_dims, out_activation

    def get_postprocessors(self):
        postprocessors = []
        if self.out_activation is None:  # if no activation is provided, we assume the output is logits
            postprocessors.append(LogitsPostprocessor())

        # if the output is binary, we add a sigmoid postprocessor, otherwise a softmax postprocessor
        if self.is_binary():
            postprocessors.append(SigmoidPostprocessor())
        else:
            postprocessors.append(SoftmaxPostprocessor())

        return postprocessors
