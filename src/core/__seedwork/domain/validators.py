''' Validators for the domain layer '''
from abc import ABC, abstractmethod
import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from rest_framework.fields import CharField, BooleanField
from rest_framework.serializers import Serializer

from .exceptions import ValidationException

@dataclass(frozen=True, slots=True)
class ValidatorRules:
    ''' Validator rules'''
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        ''' Return a new instance of ValidatorRules '''
        return ValidatorRules(value=value, prop=prop)

    def required(self) -> 'ValidatorRules':
        ''' Check if value is required '''
        if self.value is None or self.value == '':
            raise ValidationException(f'The {self.prop} is required')
        return self

    def string(self) -> 'ValidatorRules':
        ''' Check if value is a string '''
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f'The {self.prop} must be a string')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        ''' Check if value has a max length '''
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f'The {self.prop} must have a max length of {max_length}')
        return self

    def boolean(self) -> 'ValidatorRules':
        ''' Check if value is a boolean '''
        if self.value is not None and self.value is not True and self.value is not False:
            raise ValidationException(f'The {self.prop} must be a boolean')
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar('PropsValidated')


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    ''' Validator fields interface '''
    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ''' Validate data '''
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC): # pylint: disable=too-few-public-methods
    ''' DRF Validator '''

    def validate(self, data: Serializer):
        ''' Validate data '''
        serializer = data
        is_valid = serializer.is_valid()

        if not is_valid:
            self.errors = {
                field: [str(_error) for _error in _errors]
                for field, _errors in serializer.errors.items()
            }
            return False

        self.validated_data = dict(serializer.validated_data)
        return True


class StrictCharField(CharField):
    ''' Strict Char Field '''

    def to_internal_value(self, data):
        ''' To internal value '''
        if not isinstance(data, str):
            self.fail('invalid')

        return super().to_internal_value(data)


class StrictBooleanField(BooleanField):
    ''' Strict Boolean Field '''

    def to_internal_value(self, data):
        ''' To internal value '''
        with contextlib.suppress(TypeError):
            if data is True or data is False:
                return data
            elif data is None and self.allow_null:
                return None

        self.fail('invalid')

        return super().to_internal_value(data)
