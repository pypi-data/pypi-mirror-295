import torch


class Postprocessor:
    """Base class for postprocessors."""

    def postprocess(self, x):
        """Postprocess the output of the head. E.g transforming probabilities from softmax or sigmoid to class labels"""
        return x


class PostprocessorMixIn:
    """MixIn class to add postprocessing to the model."""

    def get_postprocessors(self):
        return [Postprocessor()]

    def postprocess(self, x: torch.Tensor):
        for postprocessor in self.get_postprocessors():
            x = postprocessor.postprocess(x)
        return x


class LogitsPostprocessor(Postprocessor):
    """Postprocessor for logits outputs."""

    def postprocess(self, x: torch.Tensor):
        if x.shape[-1] == 1:
            return torch.sigmoid(x)
        else:
            return torch.softmax(x, dim=-1)


class SigmoidPostprocessor(Postprocessor):
    """Postprocessor for sigmoid outputs."""

    def postprocess(self, x: torch.Tensor):
        x[x < 0.5] = 0
        x[x > 0.5] = 1
        return x


class SoftmaxPostprocessor(Postprocessor):
    """
    Postprocessor for softmax outputs.

    Parameters
    ----------
    one_hot_encoding : bool, optional, default=False
        Whether to return the output as one-hot encoded. If False, the output will be the index of the class with the highest probability.
    """

    def __init__(self, one_hot_encoding: bool = False):
        self.one_hot_encoding = one_hot_encoding

    def postprocess(self, x: torch.Tensor, **kwargs):
        idx = torch.argmax(x, dim=-1)
        if self.one_hot_encoding:
            x = torch.zeros(x.shape)
            x[torch.arange(x.shape[0]), idx] = 1
            return x
        else:
            return idx.reshape(-1, 1)
