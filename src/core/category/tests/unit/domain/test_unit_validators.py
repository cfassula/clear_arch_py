''' Unit tests for category validators '''
import unittest

from core.category.domain.validators import CategoryValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):
    '''TestCategoryValidatorUnit'''

    validator: CategoryValidator

    def setUp(self) -> None:
        '''Set up the test case'''
        self.validator = CategoryValidatorFactory().create()
        return super().setUp()

    def test_invalidations_cases_for_name_field(self):
        '''Test invalid cases for name field'''
        is_valid = self.validator.validate(None)
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], [
                             'This field is required.'])

        is_valid = self.validator.validate({})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], [
                             'This field is required.'])

        is_valid = self.validator.validate({'name': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], [
                             'This field may not be null.'])

        is_valid = self.validator.validate({'name': ''})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], [
                             'This field may not be blank.'])

        is_valid = self.validator.validate({'name': 'a' * 256})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'],
                             ['Ensure this field has no more than 255 characters.']
                             )

        is_valid = self.validator.validate({'name': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['name'], [
                             'Not a valid string.'])

    def test_invalidations_cases_for_description_field(self):
        '''Test invalid cases for description field'''
        is_valid = self.validator.validate({'name': 'test', 'description': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['description'], [
                             'Not a valid string.'])

    def test_invalidations_cases_for_is_active_field(self):
        '''Test invalid cases for is_active field'''
        is_valid = self.validator.validate({'name': 'test', 'is_active': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate({'name': 'test', 'is_active': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'This field may not be null.'])

        is_valid = self.validator.validate({'name': 'test', 'is_active': ''})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate(
            {'name': 'test', 'is_active': 'True'})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate(
            {'name': 'test', 'is_active': 'False'})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate({'name': 'test', 'is_active': '0'})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

        is_valid = self.validator.validate({'name': 'test', 'is_active': '1'})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['is_active'], [
                             'Must be a valid boolean.'])

    def test_invalidations_cases_for_created_at_field(self):
        '''Test invalid cases for created_at field'''

        is_valid = self.validator.validate(
            {'name': 'test', 'created_at': None})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['created_at'], [
                             'This field may not be null.'])

        is_valid = self.validator.validate({'name': 'test', 'created_at': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(
            self.validator.errors['created_at'], [
                'Datetime has wrong format. Use one of these formats ' +
                'instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']
        )

    def test_valid_cases(self):
        '''Test valid cases '''
        valid_data = [
            {'name': 'test'},
            {'name': 'test', 'description': None},
            {'name': 'test', 'description': ''},
            {'name': 'test', 'description': 'some description'},
            {'name': 'test', 'is_active': True},
            {'name': 'test', 'is_active': False},
            {'name': 'test', 'is_active': False,
                'description': 'some description'},
        ]

        for data in valid_data:
            is_valid = self.validator.validate(data)
            self.assertTrue(is_valid)
