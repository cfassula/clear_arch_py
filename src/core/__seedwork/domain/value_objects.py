''' Value Objects '''
from abc import ABC
from dataclasses import dataclass, field, fields
import json
import uuid
from core.__seedwork.domain.exceptions import InvalidUuidException


@dataclass(frozen=True)
class ValueObject(ABC):
    '''ValueObject base class'''

    def __str__(self) -> str:
        fields_name = [field.name for field in fields(self)]
        return str(getattr(self, fields_name[0])) \
            if len(fields_name) == 1 \
            else json.dumps({field.name: getattr(self, field.name) for field in fields(self)})


@dataclass(frozen=True)
class UniqueEntityId(ValueObject):
    ''' Unique Entity ID'''
    id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
    )

    def __post_init__(self) -> None:
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)
        self.__validate_id()

    def __validate_id(self) -> None:
        try:
            uuid.UUID(self.id, version=4)
        except ValueError as ex:
            raise InvalidUuidException() from ex
