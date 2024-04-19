# pylint: disable=no-member

import unittest
import pytest
from django.utils import timezone
from django.db import models
from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):
    def test_mapping(self):
        table_name = CategoryModel._meta.db_table # pylint: disable=protected-access
        self.assertEqual(table_name, 'categories')

        fields_name = tuple(field.name for field in CategoryModel._meta.fields) # pylint: disable=protected-access
        self.assertEqual(fields_name, ('id', 'name', 'description', 'is_active', 'created_at'))

        id_field: models.UUIDField = CategoryModel.id.field
        self.assertIsInstance(id_field, models.UUIDField)
        self.assertTrue(id_field.primary_key)
        self.assertTrue(id_field.editable)
        self.assertIsNone(id_field.db_column)
        
        name_field: models.CharField = CategoryModel.name.field
        self.assertIsInstance(name_field, models.CharField)
        self.assertIsNone(name_field.db_column)
        self.assertFalse(name_field.blank)
        self.assertFalse(name_field.null)
        self.assertEqual(name_field.max_length, 255)

        description_field: models.TextField = CategoryModel.description.field
        self.assertIsInstance(description_field, models.TextField)
        self.assertIsNone(description_field.db_column)
        self.assertFalse(description_field.blank)
        self.assertTrue(description_field.null)

        is_active_field: models.BooleanField = CategoryModel.is_active.field
        self.assertIsInstance(is_active_field, models.BooleanField)
        self.assertIsNone(is_active_field.db_column)
        self.assertFalse(is_active_field.null)

        created_at_field: models.DateTimeField = CategoryModel.created_at.field
        self.assertIsInstance(created_at_field, models.DateTimeField)
        self.assertIsNone(created_at_field.db_column)
        self.assertFalse(created_at_field.blank)

    def test_create(self):
        arrange = {
            'id': '8b3f8c4f-4a0b-4e1e-9d0b-2d2c2f4b4b4b',
            'name': 'Test Category',
            'description': 'Test Description',
            'is_active': True,
            'created_at': timezone.now()
        }
        category = CategoryModel.objects.create(**arrange)
        self.assertEqual(category.id, arrange['id'])
        self.assertEqual(category.name, arrange['name'])
        self.assertEqual(category.description, arrange['description'])
        self.assertEqual(category.is_active, arrange['is_active'])
        self.assertEqual(category.created_at, arrange['created_at'])
