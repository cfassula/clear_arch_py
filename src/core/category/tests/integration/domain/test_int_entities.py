'''Test cases for Category entity'''

import unittest

from core.__seedwork.domain.exceptions import EntityValidationException
from core.category.domain.entities import Category


class TestCategoryIntegration(unittest.TestCase):
    '''TestCategoryIntegration'''

    def test_create_with_invalid_cases_for_name_prop(self):
        '''test invalid cases for name prop'''
        invalid_data = [
            {
                'data': {'name': None},
                'expected': 'This field may not be null.'
            },
            {
                'data': {'name': ''},
                'expected': 'This field may not be blank.'
            },
            {
                'data': {'name': 5},
                'expected': 'Not a valid string.'
            },
            {
                'data': {'name': "t" * 256},
                'expected': 'Ensure this field has no more than 255 characters.'
            }
        ]

        for i in invalid_data:
            with self.assertRaises(EntityValidationException) as assert_error:
                Category(**i['data'])
            self.assertIn('name', assert_error.exception.error)
            self.assertEqual(
                assert_error.exception.error['name'],
                [i['expected']],
                f'Expected: {i["expected"]}, actual: {assert_error.exception.error["name"][0]}'
            )

    def test_create_with_invalid_cases_for_description_prop(self):
        '''test invalid cases for description prop'''
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name=None, description=5)
        self.assertEqual(['Not a valid string.'],
                         assert_error.exception.error['description'])

    def test_create_with_invalid_cases_for_is_active_prop(self):
        '''test invalid cases for is_active prop'''
        with self.assertRaises(EntityValidationException) as assert_error:
            Category(name='test', is_active=5)
        self.assertEqual(assert_error.exception.error['is_active'], [
                         'Must be a valid boolean.'])

    def test_create_with_valid_cases_for_combination_between_rules(self):
        '''test valid cases for combination between rules'''
        try:
            Category(name='test')
            Category(name='test', description=None)
            Category(name='test', description="")
            Category(name='test', is_active=False)
            Category(name='test', is_active=True)
            Category(name='test', description="Some description", is_active=True)
        except EntityValidationException as exception:
            self.fail(f'Some prop is not valid. Error {exception.error}')

    def test_update_with_invalid_cases_for_name_prop(self):
        '''test invalid cases for name prop'''
        category = Category(name='Movie')

        invalid_data = [
            {
                'data': {'name': None, 'description': None},
                'expected': 'This field may not be null.'
            },
            {
                'data': {'name': '', 'description': None},
                'expected': 'This field may not be blank.'
            },
            {
                'data': {'name': 5, 'description': None},
                'expected': 'Not a valid string.'
            },
            {
                'data': {'name': "t" * 256, 'description': None},
                'expected': 'Ensure this field has no more than 255 characters.'
            }
        ]

        for i in invalid_data:
            with self.assertRaises(EntityValidationException) as assert_error:
                category.update(**i['data'])  # NOSONAR
            self.assertIn('name', assert_error.exception.error)
            self.assertEqual(
                assert_error.exception.error['name'],
                [i['expected']],
                f'Expected: {i["expected"]}, actual: {assert_error.exception.error["name"][0]}'
            )

    def test_update_with_invalid_cases_for_description_prop(self):
        '''test invalid cases for description prop'''
        category = Category(name='test')
        with self.assertRaises(EntityValidationException) as assert_error:
            category.update(name='test2', description=5)
        self.assertEqual(assert_error.exception.error['description'], [
                         'Not a valid string.'])

    def test_update_with_valid_cases_for_combination_between_rules(self):
        '''test valid cases for combination between rules'''
        category = Category(name='test')
        try:
            category.update(name='test', description=None)
            category.update(name='test', description="")
            category.update(name='test', description="Some description")
            category.update(name='test', description="S"*255)
        except EntityValidationException as exception:
            self.fail(f'Some prop is not valid. Error {exception.error}')
