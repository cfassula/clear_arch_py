'''Exceptions for the domain layer'''

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.__seedwork.domain.validators import ErrorFields


class InvalidUuidException(Exception):
    '''Exceptions '''

    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)


class ValidationException(Exception):
    '''Exceptions'''
    # pylint: disable=unnecessary-pass
    pass


class EntityValidationException(Exception):
    '''Exceptions'''
    error: 'ErrorFields'

    def __init__(self, error: 'ErrorFields') -> None:
        self.error = error
        super().__init__('Entity Validation Error')


class LoadEntityException(Exception):
    error: 'ErrorFields'

    def __init__(self, error: 'ErrorFields') -> None:
        self.error = error
        super().__init__('Load Entity Error')

class NotFoundException(Exception):
    '''Exceptions'''
    # pylint: disable=unnecessary-pass
    pass
