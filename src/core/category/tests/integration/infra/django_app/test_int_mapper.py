# pylint: disable=no-member
import unittest
import pytest
from django.utils import timezone
from core.category.domain.entities import Category
from core.category.infra.django_app.mappers import CategoryModelMapper
from core.category.infra.django_app.models import CategoryModel

@pytest.mark.django_db()
class TestCategoryModelMapperInt(unittest.TestCase):
    def test_to_entity(self):
        created_at = timezone.now()
        model = CategoryModel(
            id='8b3f8c4f-4a0b-4e1e-9d0b-2d2c2f4b4b4b',
            name='Test Category',
            description='Test Description',
            is_active=True,
            created_at=created_at
        )
        entity = CategoryModelMapper.to_entity(model)
        self.assertEqual(str(entity.id), '8b3f8c4f-4a0b-4e1e-9d0b-2d2c2f4b4b4b')
        self.assertEqual(entity.name, 'Test Category')
        self.assertEqual(entity.description, 'Test Description')
        self.assertTrue(entity.is_active)
        self.assertEqual(entity.created_at, created_at)

    def test_to_model(self):
        created_at = timezone.now()
        entity = Category(
            unique_entity_id='8b3f8c4f-4a0b-4e1e-9d0b-2d2c2f4b4b4b',
            name='Test Category',
            description='Test Description',
            is_active=True,
            created_at=created_at
        )
        model = CategoryModelMapper.to_model(entity)
        self.assertEqual(str(model.id), '8b3f8c4f-4a0b-4e1e-9d0b-2d2c2f4b4b4b')
        self.assertEqual(model.name, 'Test Category')
        self.assertEqual(model.description, 'Test Description')
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, entity.created_at)
