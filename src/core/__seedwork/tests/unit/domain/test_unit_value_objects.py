''' Module for testing value objects '''
from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
import uuid
from core.__seedwork.domain.exceptions import InvalidUuidException
from core.__seedwork.domain.value_objects import UniqueEntityId, ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    '''Stub value object for test purposes'''
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    '''Stub value object for test purposes'''
    prop1: str
    prop2: int


class TestValueObjectUnit(unittest.TestCase):
    '''Test unit for ValueObject class'''

    def test_if_is_a_dataclass(self):
        '''Test if ValueObject is a dataclass'''
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_if_is_a_abstract_class(self):
        '''Test if ValueObject is a abstract class'''
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        ''' Test if init prop correctly'''
        vo1 = StubOneProp(prop='test')
        self.assertEqual(vo1.prop, 'test')

        vo2 = StubTwoProp(prop1='test1', prop2='test2')
        self.assertEqual(vo2.prop1, 'test1')
        self.assertEqual(vo2.prop2, 'test2')

    def test_convert_to_string(self):
        ''' Test if convert to string correctly'''
        vo1 = StubOneProp(prop='test')
        self.assertEqual(str(vo1), 'test')

        vo2 = StubTwoProp(prop1='test1', prop2='test2')
        self.assertEqual(str(vo2), '{"prop1": "test1", "prop2": "test2"}')

    def test_is_immutable(self):
        ''' Test if value object is immutable'''
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop='test')
            value_object.prop = 'new_value'


class TestUniqueEntityIdUnit(unittest.TestCase):
    '''Test unit for UniqueEntityId class'''

    def test_if_is_a_dataclass(self):
        '''Test if UniqueEntityId is a dataclass'''
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        '''Test if throw exception when uuid is invalid'''
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate_id',
            autospec=True,
            # pylint: disable=protected-access
            side_effect=UniqueEntityId._UniqueEntityId__validate_id
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId(id='invalid_id')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], 'ID must be a valid UUID')

    def test_accept_passed_uuid_in_constructor(self):
        '''Test if accept passed uuid in constructor'''
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate_id',
            autospec=True,
            # pylint: disable=protected-access
            side_effect=UniqueEntityId._UniqueEntityId__validate_id
        ) as mock_validate:
            value_object = UniqueEntityId(
                id='a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(id=uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_uuid_when_constructor_not_receive_uuid(self):
        '''Test if generate uuid when constructor not receive uuid'''
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate_id',
            autospec=True,
            # pylint: disable=protected-access
            side_effect=UniqueEntityId._UniqueEntityId__validate_id
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        ''' Test if value object is immutable'''
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'new_value'
