'''Unit test for __seedwork.domain.validators module'''
from dataclasses import fields
import unittest
from unittest.mock import MagicMock, PropertyMock, patch
from rest_framework.serializers import Serializer

from core.__seedwork.domain.exceptions import ValidationException
from core.__seedwork.domain.validators import DRFValidator, ValidatorFieldsInterface, ValidatorRules


class TestValidatorRules(unittest.TestCase):
    '''Test unit for ValidatorRules class'''

    def test_value_method(self):
        '''Test if value method return a new instance of ValidatorRules'''
        validator_rules = ValidatorRules.values('test', 'prop')
        self.assertIsInstance(validator_rules, ValidatorRules)
        self.assertEqual(validator_rules.value, 'test')
        self.assertEqual(validator_rules.prop, 'prop')

    def test_required_rule(self):
        '''Test if required rule works correctly'''

        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '', 'prop': 'prop1'}
        ]
        for i in invalid_data:
            with self.assertRaises(
                ValidationException,
                msg=f'value: {i["value"]}, prop: {i["prop"]}'
            ) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).required()
            self.assertEqual(
                f'The {i["prop"]} is required',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': 'test', 'prop': 'prop'},
            {'value': 5, 'prop': 'prop1'},
            {'value': 0, 'prop': 'prop2'},
            {'value': True, 'prop': 'prop2'},
            {'value': False, 'prop': 'prop3'},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).required(),
                ValidatorRules
            )

    def test_string_rule(self):
        '''Test if string rule works correctly'''

        invalid_data = [
            {'value': 5, 'prop': 'prop'},
            {'value': 0, 'prop': 'prop1'},
            {'value': True, 'prop': 'prop2'},
            {'value': False, 'prop': 'prop3'},
            {'value': {}, 'prop': 'prop3'},
        ]
        for i in invalid_data:
            with self.assertRaises(
                ValidationException,
                msg=f'value: {i["value"]}, prop: {i["prop"]}'
            ) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).string()
            self.assertEqual(
                f'The {i["prop"]} must be a string',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': 'test', 'prop': 'prop'},
            {'value': '', 'prop': 'prop1'},
            {'value': None, 'prop': 'prop2'},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).string(),
                ValidatorRules
            )

    def test_max_length_rule(self):
        '''Test if max_length rule works correctly'''

        invalid_data = [
            {'value': 't' * 5, 'prop': 'prop', 'max_length': 4},
        ]
        for i in invalid_data:
            with self.assertRaises(
                ValidationException,
                msg=f'value: {i["value"]}, prop: {i["prop"]}'
            ) as assert_error:
                ValidatorRules.values(
                    i['value'], i['prop']).max_length(i['max_length'])
            self.assertEqual(
                f'The {i["prop"]} must have a max length of {i["max_length"]}',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': 'test', 'prop': 'prop', 'max_length': 4},
            {'value': 'test', 'prop': 'prop1', 'max_length': 5},
            {'value': 'test', 'prop': 'prop2', 'max_length': 10},
            {'value': 'test', 'prop': 'prop3', 'max_length': 100},
            {'value': '', 'prop': 'prop4', 'max_length': 100},
            {'value': None, 'prop': 'prop5', 'max_length': 100},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(
                    i['value'], i['prop']).max_length(i['max_length']),
                ValidatorRules
            )

    def test_boolean_rule(self):
        '''Test if boolean rule works correctly'''

        invalid_data = [
            {'value': 'test', 'prop': 'prop'},
            {'value': 5, 'prop': 'prop1'},
            {'value': 0, 'prop': 'prop2'},
            {'value': '', 'prop': 'prop3'},
            {'value': {}, 'prop': 'prop5'},
        ]
        for i in invalid_data:
            with self.assertRaises(
                ValidationException,
                msg=f'value: {i["value"]}, prop: {i["prop"]}'
            ) as assert_error:
                ValidatorRules.values(i['value'], i['prop']).boolean()
            self.assertEqual(
                f'The {i["prop"]} must be a boolean',
                assert_error.exception.args[0],
            )

        valid_data = [
            {'value': None, 'prop': 'prop4'},
            {'value': True, 'prop': 'prop'},
            {'value': False, 'prop': 'prop1'},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i['value'], i['prop']).boolean(),
                ValidatorRules
            )

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        '''Test if throw a ValidationException when combine two or more rules'''
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop must be a string',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                "t" * 6,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop must have a max length of 5',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5,
                'prop'
            ).required().boolean()
        self.assertEqual(
            'The prop must be a boolean',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().boolean()
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

    def test_valid_cases_for_combination_between_rules(self):
        '''Test valid cases for combination between rules'''
        ValidatorRules(
            'test',
            'prop'
        ).required().string()

        ValidatorRules(
            "t" * 5,
            'prop'
        ).required().string().max_length(5)

        ValidatorRules(
            True,
            'prop'
        ).required().boolean()

        ValidatorRules(
            False,
            'prop'
        ).required().boolean()

        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)


class TestValidatorFieldsInterface(unittest.TestCase):
    '''Test unit for ValidatorFieldsInterface class'''

    def test_throw_not_implemented_error(self):
        '''Test if validate method raise NotImplementedError'''
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class ValidatorFieldsInterface " +
            "with abstract method validate"
        )

    def test_qualquer(self):
        '''Test if fields method return a list of fields with errors and validated_data fields'''

        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)


class TestDRFValidatorUnit(unittest.TestCase):
    '''Test unit for DRFValidator class'''

    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(
        Serializer,
        'validated_data',
        return_value={'field': ['value']},
        new_callable=PropertyMock
    )
    def test_if_validated_data_is_set(
        self,
        mock_errors: PropertyMock,
        mock_is_valid: MagicMock
    ):
        '''Test if validate method works correctly'''

        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        mock_errors.assert_called()
        self.assertTrue(is_valid)
        mock_is_valid.assert_called_once()
        self.assertEqual(validator.validated_data, {'field': ['value']})

    @patch.object(Serializer, 'is_valid', return_value=False)
    @patch.object(
        Serializer,
        'errors',
        return_value={'field': ['some error']},
        new_callable=PropertyMock
    )
    def test_if_erros_is_set(
        self,
        mock_errors: PropertyMock,
        mock_is_valid: MagicMock
    ):
        '''Test if errors works correctly'''

        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        mock_errors.assert_called()
        self.assertFalse(is_valid)
        mock_is_valid.assert_called_once()
        self.assertEqual(validator.errors, {'field': ['some error']})
