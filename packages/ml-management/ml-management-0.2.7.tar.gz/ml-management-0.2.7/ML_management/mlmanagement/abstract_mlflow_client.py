"""Define abstract mlflow client."""

from abc import abstractmethod

from mlflow.entities import Run


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
