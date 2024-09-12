from amsdal_models.enums import MetaClasses as MetaClasses
from amsdal_models.schemas.data_models.core import TypeData as TypeData
from pydantic import BaseModel, Field as Field
from typing import Annotated, Any

class OptionItemData(BaseModel):
    key: str
    value: Any

class PropertyData(TypeData, extra='allow'):
    """
    Schema for property data.

    This class represents the schema for property data, which extends the TypeData class
    and includes additional attributes such as title, options, read-only status, field name,
    field ID, and deletion status.

    Attributes:
        title (str | None): The title of the property.
        options (list[OptionItemData] | None): A list of option item data.
        read_only (bool): Indicates if the property is read-only.
        field_name (str | None): The name of the field.
        field_id (str | None): The ID of the field.
        is_deleted (bool): Indicates if the property is deleted.
    """
    title: str | None
    options: list[OptionItemData] | None
    read_only: bool
    field_name: str | None
    field_id: str | None
    is_deleted: bool

class ObjectSchema(BaseModel, extra='allow'):
    """
    Schema for an object.

    This class represents the schema for an object, including attributes such as title, type,
    required properties, default value, properties, options, meta class, and custom code.

    Attributes:
        title (Annotated\\[str, Field\\]): The title of the object, with a minimum length of 1 and a maximum length of 255
        type (str): The type of the object, default is 'object'.
        required (Annotated\\[list\\[str\\], Field\\]): A list of required property names.
        default (Any): The default value for the object.
        properties (dict\\[str, PropertyData\\] | None): A dictionary of property data.
        options (list\\[OptionItemData\\] | None): A list of option item data.
        meta_class (str): The meta class of the object, default is the value of MetaClasses.CLASS_OBJECT.
        custom_code (str | None): Custom code associated with the object.
    """
    title: Annotated[str, None]
    type: str
    required: Annotated[list[str], None]
    default: Any
    properties: dict[str, PropertyData] | None
    options: list[OptionItemData] | None
    meta_class: str
    custom_code: str | None
    def __hash__(self) -> int: ...
