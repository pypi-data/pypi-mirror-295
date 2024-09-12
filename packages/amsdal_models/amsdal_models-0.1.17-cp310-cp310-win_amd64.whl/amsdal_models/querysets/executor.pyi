import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from amsdal_data.connections.base import ConnectionBase
from amsdal_models.querysets.base_queryset import QuerySetBase as QuerySetBase
from amsdal_utils.models.data_models.address import Address
from typing import Any

logger: Incomplete
DEFAULT_DB_ALIAS: str
LAKEHOUSE_DB_ALIAS: str

class ExecutorBase(ABC, metaclass=abc.ABCMeta):
    """
    Abstract base class for query executors.

    This class provides the base functionality for executing queries and counting
    results. It defines the interface that all concrete executor classes must implement.

    Attributes:
        queryset (QuerySetBase): The query set to be executed.
    """
    queryset: QuerySetBase
    _config_manager: Incomplete
    def __init__(self, queryset: QuerySetBase) -> None: ...
    def _get_connection_name(self) -> str: ...
    def _get_connection(self) -> ConnectionBase: ...
    @abstractmethod
    def query(self) -> list[dict[str, Any]]: ...
    @abstractmethod
    def count(self) -> int: ...

class Executor(ExecutorBase):
    """
    Concrete executor class for executing queries and counting results.

    This class extends the `ExecutorBase` and provides the implementation for
    executing queries and counting results using the specified query set.
    """
    def _address(self) -> Address: ...
    def query(self) -> list[dict[str, Any]]:
        """
        Execute the query and return the results.

        This method uses the connection object to execute the query based on the
        query set's specifier, conditions, pagination, and order by attributes.

        Returns:
            list[dict[str, Any]]: The query results as a list of dictionaries.
        """
    def count(self) -> int:
        """
        Execute the query and return the count of results.

        This method uses the connection object to execute the query and return
        the count of model instances that match the query conditions.

        Returns:
            int: The count of matching results.
        """
