"""Abstract base class for model transformation methods."""
from abc import ABC, abstractmethod
from typing import Callable

from ML_management.mlmanagement.jsonschema_inference import SkipJsonSchema
from ML_management.model.patterns.model_pattern import Model


class Transformer(Model, ABC):
    """Abstract class for model that performs transformations."""

    @abstractmethod
    def transform(self, model_fn: SkipJsonSchema[Callable], **kwargs) -> Callable:
        """Perform model transformation.

        :param model_fn: takes a batch of input tensors and produces a final prediction tensor.
        """
        raise NotImplementedError
