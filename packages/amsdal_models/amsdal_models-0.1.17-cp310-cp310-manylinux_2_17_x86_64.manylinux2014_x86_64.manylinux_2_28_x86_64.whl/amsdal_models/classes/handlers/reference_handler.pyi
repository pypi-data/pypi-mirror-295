import typing_extensions
from amsdal_models.classes.constants import REFERENCE_FIELD_SUFFIX as REFERENCE_FIELD_SUFFIX
from amsdal_models.classes.handlers.object_id_handler import ObjectIdHandler as ObjectIdHandler
from typing import Any, Literal

IncEx: typing_extensions.TypeAlias

class ReferenceHandler(ObjectIdHandler):
    _serialize_with_refs: bool
    _exclude_none: bool
    def ser_model(self) -> dict[str, Any]:
        """
        Serializes the model.

        Returns:
            dict[str, Any]: The serialized model as a dictionary.
        """
    def model_dump_refs(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ...) -> dict[str, Any]:
        """
        Dumps the model with references.

        Args:
            mode (Literal['json', 'python'] | str, optional): The mode of serialization. Defaults to 'python'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.

        Returns:
            dict[str, Any]: The serialized model as a dictionary.
        """
    def model_dump(self, *, mode: Literal['json', 'python'] | str = ..., include: IncEx = ..., exclude: IncEx = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ...) -> dict[str, Any]:
        """
        Dumps the model.

        Args:
            mode (Literal['json', 'python'] | str, optional): The mode of serialization. Defaults to 'python'.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.

        Returns:
            dict[str, Any]: The serialized model as a dictionary.
        """
    def model_dump_json_refs(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ...) -> str:
        """
        Dumps the model as a JSON string with references.

        Args:
            indent (int | None, optional): The number of spaces to use for indentation. Defaults to None.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.

        Returns:
            str: The serialized model as a JSON string.
        """
    def model_dump_json(self, *, indent: int | None = ..., include: IncEx = ..., exclude: IncEx = ..., by_alias: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., round_trip: bool = ..., warnings: bool = ...) -> str:
        """
        Dumps the model as a JSON string.

        Args:
            indent (int | None, optional): The number of spaces to use for indentation. Defaults to None.
            include (IncEx, optional): Fields to include in the serialization. Defaults to None.
            exclude (IncEx, optional): Fields to exclude from the serialization. Defaults to None.
            by_alias (bool, optional): Whether to use field aliases. Defaults to False.
            exclude_unset (bool, optional): Whether to exclude unset fields. Defaults to False.
            exclude_defaults (bool, optional): Whether to exclude fields with default values. Defaults to False.
            exclude_none (bool, optional): Whether to exclude fields with None values. Defaults to False.
            round_trip (bool, optional): Whether to ensure round-trip serialization. Defaults to False.
            warnings (bool, optional): Whether to show warnings. Defaults to True.

        Returns:
            str: The serialized model as a JSON string.
        """
