from amsdal.errors import AmsdalAuthenticationError as AmsdalAuthenticationError
from amsdal_data.connections.base import ConnectionBase
from amsdal_data.connections.historical_base import HistoricalConnectionBase
from amsdal_data.connections.state_base import StateConnectionBase
from amsdal_data.operations.enums import OperationType
from amsdal_data.operations.manager import OperationsManagerBase
from amsdal_models.classes.model import Model
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.metadata import Metadata as Metadata
from typing import Any

class OperationsManager(OperationsManagerBase):
    """
    Manages operations for models, including state and historical operations.
    """
    def _get_connections(self, obj: Model, using: str | None) -> list[ConnectionBase]: ...
    def _perform_state_operation(self, obj: Model, data_dump: dict[str, Any], operation: OperationType, connection: StateConnectionBase) -> None: ...
    @classmethod
    def clear_data(cls, _value: Any) -> Any:
        """
        Clears data by recursively processing dictionaries, lists, and enums.

        Returns:
            Any: The cleared value.
        """
    def _is_reference(self, _value: Any) -> bool: ...
    def _perform_historical_operation(self, obj: Model, data_dump: dict[str, Any], operation: OperationType, connection: HistoricalConnectionBase) -> None: ...
    def _preprocess_object(self, obj: Model, operation: OperationType) -> None: ...
    def perform_operation(self, obj: Model, operation: OperationType, using: str | None = None) -> None:
        """
        Performs the specified operation on the given model object.

        Args:
            obj (Model): The model object.
            operation (OperationType): The type of operation to perform.
            using (str | None, optional): The database alias to use. Defaults to None.

        Returns:
            None
        """
    def _generate_references(self, address: Address, data: Any, reference_buffer: list[tuple[Address, dict[str, Any]]]) -> None: ...
    def _perform_historical_bulk_operation(self, objects_data: list[tuple[Model, dict[str, Any]]], operation: OperationType, connection: HistoricalConnectionBase) -> None: ...
    def _perform_state_bulk_operation(self, objects_data: list[tuple[Model, dict[str, Any]]], operation: OperationType, connection: StateConnectionBase) -> None: ...
    def perform_bulk_operation(self, objs: list[Model], operation: OperationType, using: str | None = None) -> None:
        """
        Performs the specified bulk operation on the given model objects.

        Args:
            objs (list[Model]): The list of model objects.
            operation (OperationType): The type of operation to perform.
            using (str | None, optional): The database alias to use. Defaults to None.
        """
