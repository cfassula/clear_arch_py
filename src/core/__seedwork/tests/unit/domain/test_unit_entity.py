''' Test unit for Entity class '''
from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest

from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    '''Stub entity for test purposes'''
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    '''Test unit for Entity class'''

    def test_if_is_a_dataclass(self):
        '''Test if Entity is a dataclass'''
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self):
        '''Test if Entity is a abstract class'''
        self.assertIsInstance(Entity(), ABC)

    def test_set_id_and_props(self):
        '''Test if set id and props correctly'''
        entity = StubEntity(prop1='test1', prop2='test2')
        self.assertEqual(entity.prop1, 'test1')
        self.assertEqual(entity.prop2, 'test2')
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_if_accept_a_uuid_valid(self):
        '''Test if accept a valid uuid'''
        entity = StubEntity(
            unique_entity_id=UniqueEntityId(
                id='a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
            prop1='test1',
            prop2='test2'
        )

        self.assertEqual(entity.id, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')

    def test_to_dict_method(self):
        '''Test if to_dict method return a dict with entity properties'''
        entity = StubEntity(
            unique_entity_id=UniqueEntityId(
                id='a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
            prop1='test1',
            prop2='test2'
        )
        self.assertDictEqual(entity.to_dict(), {
            'id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
            'prop1': 'test1',
            'prop2': 'test2'
        })
