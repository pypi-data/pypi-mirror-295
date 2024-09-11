from abc import ABC, abstractmethod
from enum import Enum


class TypesFields(ABC):
    @abstractmethod
    def __str__(self) -> str:
        ...


class IntegerField(TypesFields):
    def __str__(self) -> str:
        return "int"


class CharField(TypesFields):
    def __str__(self) -> str:
        return "varchar"


class BoolField(TypesFields):
    def __str__(self) -> str:
        return "boolean"


class DateField(TypesFields):
    def __str__(self) -> str:
        return "data"


class DateTimeField(TypesFields):
    def __str__(self) -> str:
        return "datatime"


class TimeField(TypesFields):
    def __str__(self) -> str:
        return "time"


class TimeStampField(TypesFields):
    def __str__(self) -> str:
        return "timestamp"


class YearField(TypesFields):
    def __str__(self) -> str:
        return "year"


class TextField(TypesFields):
    def __str__(self) -> str:
        return "text"


class BlobField(TypesFields):
    def __str__(self) -> str:
        return "blob"


class JSON(TypesFields):
    def __str__(self) -> str:
        return "json"


class TypesEnum(Enum):
    IntegerField = IntegerField
    CharField = CharField
    BoolField = BoolField
    DateField = DateField
    DateTimeField = DateTimeField
    TimeField = TimeField
    TimeStampField = TimeStampField
    YearField = YearField
    TextField = TextField
    BlobField = BlobField
    JSON = JSON
