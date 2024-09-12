"""Class inherits from base class of Model with a specific method for updating and computing metrics."""
from abc import ABC, abstractmethod
from typing import Dict

from ML_management.mlmanagement.jsonschema_inference import SkipJsonSchema
from ML_management.model.patterns.model_pattern import Model


class ModelWithMetrics(Model, ABC):
    """Implementation of model with specific methods for reseting, updating and computing metrics."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def reset_metrics(self) -> None:
        """Define function to reset internal variables."""
        raise NotImplementedError

    @abstractmethod
    def update_metrics(self, outputs_batch: SkipJsonSchema["tensor"], targets: SkipJsonSchema["tensor"], **kwargs) -> None:  # type: ignore # noqa
        """Define function to update internal variables with provided (outputs_batch, targets)."""
        raise NotImplementedError

    @abstractmethod
    def compute_metrics(self, **kwargs) -> Dict[str, float]:
        """Define function to compute the metrics and return the results in dictionary format."""
        raise NotImplementedError
