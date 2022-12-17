from dataclasses import is_dataclass, asdict, dataclass
from enum import Enum
from json import JSONEncoder, loads, dumps
from typing import Optional

from arrow import Arrow
from bson import ObjectId
from invoice.enums import CurrencyCode


class EnhancedJSONEncoder(JSONEncoder):

    def default(self, o):
        if is_dataclass(o):
            return asdict(o)

        elif isinstance(o, ObjectId):
            return str(o)

        elif isinstance(o, Arrow):
            return str(o)

        elif isinstance(o, Enum):
            return o.value

        return super().default(o)


class DataClassMeta(type):

    def __call__(cls, *args, **kwargs):
        if '_id' in kwargs:
            _id = kwargs.pop('_id')
            kwargs['id'] = _id

        return super().__call__(*args, **kwargs)


class DataClass(metaclass=DataClassMeta):

    def to_json(self, insert_mode: bool = False, include: list = None, exclude: list = None) -> dict:
        """Convert dataclass to json

        Keyword Arguments:
            insert_mode (bool) -- Exclude the ID (default False)
            include (list) -- Include the specified keys (default None)
            exclude (list) -- Exclude the specified keys (default None)
        
        Returns:
            dict
        """

        data = loads(dumps(self, cls=EnhancedJSONEncoder))

        _exclude = exclude or []

        if insert_mode:
            _exclude.append('id')

        if include:
            result_fields = {}
            for field_name in include:
                result_fields[field_name] = data.get(field_name)
            return result_fields

        for excluded_field in _exclude:
            data.pop(excluded_field, None)

        return data


@dataclass
class Contact(DataClass):
    uniqueId: str
    name: str
    organization: str
    iban: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    id: Optional[str] = None


@dataclass
class InvoiceAmount(DataClass):
    currencyCode: CurrencyCode
    value: float


@dataclass
class Invoice(DataClass):
    invoiceDate: str
    invoiceId: str
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    id: Optional[str] = None
