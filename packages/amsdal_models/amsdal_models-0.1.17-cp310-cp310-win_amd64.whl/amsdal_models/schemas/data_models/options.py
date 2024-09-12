from typing import Annotated

from pydantic import BaseModel
from pydantic import Field

from amsdal_models.schemas.data_models.schema import OptionItemData


class OptionSchema(BaseModel):
    """
    Schema for an option.

    This class represents the schema for an option, including the title and the values.

    Attributes:
        title (Annotated[str, Field]): The title of the option, with a minimum length of 1 and a maximum length of 255.
        values (list[OptionItemData]): A list of option item data.
    """

    title: Annotated[str, Field(..., min_length=1, max_length=255)]
    values: list[OptionItemData]
