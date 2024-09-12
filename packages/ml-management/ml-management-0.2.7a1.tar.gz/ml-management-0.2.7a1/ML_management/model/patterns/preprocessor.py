"""Abstract base class for preprocessing methods."""
from abc import ABC, abstractmethod

from ML_management.mlmanagement.jsonschema_inference import SkipJsonSchema
from ML_management.model.patterns.model_pattern import Model


class Preprocessor(Model, ABC):
    """Abstract class for model that performs preprocessing."""

    @abstractmethod
    def preprocess(self, input_batch: SkipJsonSchema["tensor"], **kwargs) -> "tensor":  # type: ignore # noqa
        """Perform data preprocessing."""
        raise NotImplementedError

    def predict_function(self, input_batch: SkipJsonSchema["tensor"]):  # type: ignore # noqa
        return self.preprocess(input_batch)
