from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.mixin import QueryableMixin
from amsdal_utils.query.utils import Q


class ReferenceData(Address, validate_assignment=True):
    pass


class Reference(QueryableMixin, BaseModel, populate_by_name=True):
    """
    Represents a reference to an object/record.

    Attributes:
        ref (ReferenceData): The reference to the object/record.
    """

    ref: ReferenceData = Field(alias='$ref')

    @field_validator('ref', mode='before')
    @classmethod
    def set_address(cls, address: str | Address | dict[str, str]) -> ReferenceData:
        """
        Validates and sets the address for the reference data.

        Args:
            address (str | Address | dict[str, str]): The address to set. It can be a string, an Address instance,
                or a dictionary.

        Returns:
            ReferenceData: The validated reference data.

        Raises:
            ValueError: If the input is not a valid dictionary or instance of ReferenceData.
            ValueError: If the class version is not provided or is set to Versions.ALL.
            ValueError: If the object version is set to Versions.ALL.
        """
        if isinstance(address, Address):
            ref = ReferenceData.from_string(address.to_string())
        elif isinstance(address, str):
            ref = ReferenceData.from_string(address)
        else:
            try:
                ref = ReferenceData(**address)
            except TypeError as exc:
                msg = 'Input should be a valid dictionary or instance of ReferenceData'
                raise ValueError(msg) from exc

        if not ref.class_version:
            msg = 'Class version is required.'
            raise ValueError(msg)

        if isinstance(ref.class_version, Versions) and ref.class_version == Versions.ALL:
            msg = 'Class version cannot be ALL.'
            raise ValueError(msg)

        if isinstance(ref.object_version, Versions) and ref.object_version == Versions.ALL:
            msg = 'Object version cannot be ALL.'
            raise ValueError(msg)

        if not ref.object_version:
            ref.object_version = Versions.LATEST

        if ref.object_version == Versions.LATEST:
            ref.class_version = Versions.LATEST

        return ref

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """
        Dumps the model data to a dictionary.

        Args:
            **kwargs (Any): Additional keyword arguments to pass to the model dump.

        Returns:
            dict[str, Any]: A dictionary representation of the model data.
        """
        # we always use Reference with aliased prop $ref
        data = dict(kwargs.items())
        data['by_alias'] = False
        return super().model_dump(**data)

    def to_query(self, prefix: str = '') -> Q:
        """
        Converts the reference data to a query object.

        Args:
            prefix (str): The prefix to use for the query fields. Defaults to an empty string.

        Returns:
            Q: The query object representing the reference data.
        """
        return self.ref.to_query(prefix=f'{prefix}ref__')

    def __hash__(self) -> int:
        return hash(self.ref)
