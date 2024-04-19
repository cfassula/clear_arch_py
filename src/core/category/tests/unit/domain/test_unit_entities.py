'''TestCategory unit test'''
from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
from time import sleep
import unittest
from unittest.mock import patch

from core.category.domain.entities import Category


class TestCategory(unittest.TestCase):
    '''TestCategory unit test'''

    def test_if_is_a_dataclass(self):
        '''test if is a dataclass'''
        self.assertTrue(is_dataclass(Category))

    def test_is_immutable(self):
        '''test if is immutable'''
        with self.assertRaises(FrozenInstanceError):
            category = Category(name="test")
            category.name = 'new_value'

    def test_category_constructor(self):
        '''test constructor'''
        with patch.object(Category, 'validate') as mock_validate_method:
            category = Category(name="test")
            mock_validate_method.assert_called_once()
            self.assertEqual(category.name, "test")
            self.assertIsNone(category.description)
            self.assertTrue(category.is_active)
            self.assertIsInstance(category.created_at, datetime)

            created_at = datetime.now()
            category = Category(
                name="test",
                description="some test",
                is_active=False,
                created_at=created_at)

            self.assertEqual(category.name, "test")
            self.assertEqual(category.description, "some test")
            self.assertFalse(category.is_active)
            self.assertEqual(category.created_at, created_at)

    def test_if_created_is_generated_in_constructor(self):
        ''' test if created_at is generated in constructor'''

        with patch.object(Category, 'validate'):
            category1 = Category(name="test1")
            sleep(0.1)
            category2 = Category(name="test 2")
            self.assertNotEqual(
                category1.created_at.timestamp(),
                category2.created_at.timestamp()
            )

    def test_update(self):
        '''update test'''
        with patch.object(Category, 'validate'):
            category = Category(name="test")
            category.update(name="new name", description="new description")
            self.assertEqual(category.name, "new name")
            self.assertEqual(category.description, "new description")

    def test_activate(self):
        '''activate test'''
        with patch.object(Category, 'validate'):
            category = Category(name="test", is_active=False)
            category.activate()
            self.assertTrue(category.is_active)

    def test_deactivate(self):
        '''deactivate test '''
        with patch.object(Category, 'validate'):
            category = Category(name="test", is_active=True)
            category.deactivate()
            self.assertFalse(category.is_active)
