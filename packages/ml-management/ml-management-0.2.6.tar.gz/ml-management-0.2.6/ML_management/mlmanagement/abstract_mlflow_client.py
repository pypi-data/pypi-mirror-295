"""Define abstract mlflow client."""

from abc import abstractmethod
from typing import Optional

from mlflow.entities import Experiment, Run


class AbstractMlflowClient:
    """Initialize an MLflow Client."""

    @abstractmethod
    def get_run(self, *args, **kwargs) -> Run:
        """Get run by id."""
        raise NotImplementedError

    @abstractmethod
    def set_terminated(self, *args, **kwargs) -> None:
        """Set a run’s status to terminated."""
        raise NotImplementedError

    @abstractmethod
    async def get_experiment_by_name(self, *args, **kwargs) -> Optional[Experiment]:
        """Retrieve an experiment by experiment name from the backend store."""
        raise NotImplementedError

    @abstractmethod
    def get_experiment(self, *args, **kwargs) -> Experiment:
        """Get experiment by it's id."""
        raise NotImplementedError
