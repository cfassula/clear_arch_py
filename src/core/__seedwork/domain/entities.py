'''
entities.py
'''

from abc import ABC
from dataclasses import Field, dataclass, field, asdict
from typing import Any

from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class Entity(ABC):
    '''
    Abstract class
    '''
    unique_entity_id: UniqueEntityId = field(
        # pylint: disable=unnecessary-lambda
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self):
        '''
        string id
        '''
        return str(self.unique_entity_id)

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self

    def to_dict(self):
        '''
        dict
        '''
        entity_dict = asdict(self)
        entity_dict.pop('unique_entity_id')
        entity_dict['id'] = self.id
        return entity_dict

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        ''' Get field '''
        # pylint: disable=no-member
        return cls.__dataclass_fields__[entity_field]
