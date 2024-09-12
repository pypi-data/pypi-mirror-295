from abc import abstractmethod

from pydantic import BaseModel

from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.query.mixin import QueryableMixin
from amsdal_utils.query.utils import Q


class ModelBase(QueryableMixin, BaseModel):  # pragma: no cover
    @abstractmethod
    def get_metadata(self) -> Metadata: ...

    """
    Retrieves the metadata for the model.

    Returns:
        Metadata: The metadata associated with the model.
    """

    def to_query(self, prefix: str = '', *, force_frozen: bool = False) -> Q:
        """
        Converts the model metadata to a query object.

        Args:
            prefix (str): The prefix to use for the query. Defaults to an empty string.
            force_frozen (bool): Whether to force the query to be frozen. Defaults to False.

        Returns:
            Q: The query object.
        """
        return self.get_metadata().to_query(prefix, force_frozen=force_frozen)
