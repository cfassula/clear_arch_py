'''
entities.py
'''
import datetime
from dataclasses import dataclass, field
from typing import Optional

from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.exceptions import EntityValidationException
from core.category.domain.validators import CategoryValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    '''
    class

    '''
    # pylint: disable=unnecessary-lambda
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime.datetime] = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    '''
    RETIRADO POIS É UM PURISMO DEMASIADO GRANDE PEGAR OS VALORES 
    ANTES DA INSTANCIA SER CRIADA E VALIDAR. PODEMOS APLICAR A 
    VALIDAÇÃO NO __post_init__ POIS SE DER ERRO NÃO DARA SEQUENCIA 
    NO PROCESSO
    '''
    # def __new__(cls, **kwargs):
    #     cls.validate(
    #         name=kwargs.get('name'),
    #         description=kwargs.get('description'),
    #         is_active=kwargs.get('is_active'),
    #         created_at=kwargs.get('created_at')
    #     )
    #     return super(Category, cls).__new__(cls)

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.datetime.now(
                datetime.timezone.utc))
        self.validate()

    def update(self, name: str, description: str):
        '''
        update
        '''
        self._set('name', name)
        self._set('description', description)
        self.validate()
        return self

    def activate(self):
        '''
        Activate
        '''
        self._set('is_active', True)

    def deactivate(self):
        '''Deactivate'''
        self._set('is_active', False)

    # def validate(cls, name: str, description: str, is_active: bool = None ):
    #     '''validate'''
    # @classmethod
    #     ValidatorRules.values(name, 'name').required().string().max_length(255)
    #     ValidatorRules.values(description, 'description').string()
    #     ValidatorRules.values(is_active, 'is_active').boolean()

    def validate(self):
        '''validate'''
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)

    @staticmethod
    def fake():
        from core.category.domain.entity_fake_builder import CategoryFakerBuilder # pylint: disable=import-outside-toplevel
        return CategoryFakerBuilder
