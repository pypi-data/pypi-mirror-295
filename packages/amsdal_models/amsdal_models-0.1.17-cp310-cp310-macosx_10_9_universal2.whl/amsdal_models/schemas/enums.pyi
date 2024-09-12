from enum import Enum

class CoreTypes(str, Enum):
    """
    Enumeration of core data types.

    This enum class defines the core data types used in the schema definitions.

    Attributes:
        NUMBER (str): Represents a numeric type.
        STRING (str): Represents a string type.
        BOOLEAN (str): Represents a boolean type.
        DICTIONARY (str): Represents a dictionary type.
        ARRAY (str): Represents an array type.
        ANYTHING (str): Represents any type.
        BINARY (str): Represents a binary type.
        OBJECT (str): Represents an object type.
        DATETIME (str): Represents a datetime type.
        DATE (str): Represents a date type.
    """
    NUMBER: str
    STRING: str
    BOOLEAN: str
    DICTIONARY: str
    ARRAY: str
    ANYTHING: str
    BINARY: str
    OBJECT: str
    DATETIME: str
    DATE: str
