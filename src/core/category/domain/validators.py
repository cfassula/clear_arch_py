''' This module contains the validators for the category domain '''

from typing import Any
from rest_framework import serializers

from core.__seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField

# pylint: disable=abstract-method


class CategoryRules(serializers.Serializer):
    ''' Category rules '''
    name = StrictCharField(max_length=255)
    description = StrictCharField(
        required=False, allow_null=True, allow_blank=True)
    is_active = StrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):
    ''' Category validator '''

    def validate(self, data: Any) -> bool:
        ''' Validate data '''
        rules = CategoryRules(data=data if data is not None else {})
        return super().validate(rules)


class CategoryValidatorFactory:
    ''' Category validator factory '''
    @staticmethod
    def create() -> CategoryValidator:
        ''' Create a new category validator '''
        return CategoryValidator()
