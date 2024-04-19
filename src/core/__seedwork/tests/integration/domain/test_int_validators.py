''' Integration tests for validators. '''
import unittest

from rest_framework import serializers

from core.__seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField

# pylint: disable=abstract-method


class StubSerializer(serializers.Serializer):
    ''' Stub serializer for testing DRFValidator. '''
    name = serializers.CharField()
    price = serializers.IntegerField()


class TestDRFValidatorIntegration(unittest.TestCase):
    ''' Integration tests for DRFValidator. '''

    def test_validation_with_error(self):
        ''' Should return False and set errors when validation fails. '''

        validator = DRFValidator()
        serializer = StubSerializer(data={})

        is_valid = validator.validate(serializer)
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {
            'name': ['This field is required.'],
            'price': ['This field is required.']
        })

    def test_validation_with_success(self):
        ''' Should return True and set validated_data when validation succeeds. '''

        validator = DRFValidator()
        serializer = StubSerializer(data={'name': 'Product', 'price': 10})

        is_valid = validator.validate(serializer)
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {
                         'name': 'Product', 'price': 10})


class TestStrictCharFieldUnit(unittest.TestCase):
    '''Test unit for StrictCharField class'''

    def test_if_is_invalid_when_not_char_field(self):
        '''Test if strict char field works correctly'''
        class StubStrictCharFieldSerializer(serializers.Serializer):
            '''Stub strict char field serializer'''
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 10})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

        serializer = StubStrictCharFieldSerializer(data={'name': True})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'name': [serializers.ErrorDetail(string='Not a valid string.', code='invalid')]
        })

    def test_if_none_value_is_valid(self):
        '''Test if strict char field works correctly'''
        class StubStrictCharFieldSerializer(serializers.Serializer):
            '''Stub strict char field serializer'''
            name = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(data={'name': None})
        self.assertTrue(serializer.is_valid())

    def test_value_valid(self):
        '''Test if strict char field works correctly'''
        class StubStrictCharFieldSerializer(serializers.Serializer):
            '''Stub strict char field serializer'''
            name = StrictCharField()

        serializer = StubStrictCharFieldSerializer(data={'name': 'Some Name'})
        self.assertTrue(serializer.is_valid())


class TestStrictBooleanFieldUnit(unittest.TestCase):
    '''Test unit for StrictBooleanField class'''

    def test_if_is_invalid_when_not_char_field(self):
        '''Test if strict char field works correctly'''
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            '''Stub strict char field serializer'''
            active = StrictBooleanField()

        serializer = StubStrictBooleanFieldSerializer(data={'active': 0})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 1})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'True'})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

        serializer = StubStrictBooleanFieldSerializer(data={'active': 'False'})
        serializer.is_valid()
        self.assertEqual(serializer.errors, {
            'active': [serializers.ErrorDetail(string='Must be a valid boolean.', code='invalid')]
        })

    def test_if_none_value_is_valid(self):
        '''Test if strict char field works correctly'''
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            '''Stub strict char field serializer'''
            active = StrictBooleanField(allow_null=True)

        serializer = StubStrictBooleanFieldSerializer(data={'active': None})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': True})
        self.assertTrue(serializer.is_valid())

        serializer = StubStrictBooleanFieldSerializer(data={'active': False})
        self.assertTrue(serializer.is_valid())
