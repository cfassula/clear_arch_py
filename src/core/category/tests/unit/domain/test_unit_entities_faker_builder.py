
from datetime import datetime
import unittest

from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entity_fake_builder import CategoryFakerBuilder


class TestCategoryFakerBuilder(unittest.TestCase):

    def test_unique_entity_id_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_error:
            faker = CategoryFakerBuilder.a_category()
            faker.unique_entity_id  # pylint: disable=pointless-statement
        self.assertEqual(
            str(assert_error.exception),
            'Prop unique_entity_id not have a factory, use "with methods" to set a value'
        )

    def test_unique_entity_id_prop(self):
        faker = CategoryFakerBuilder.a_category()
        unique_entity_id = UniqueEntityId()
        this = faker.with_unique_entity_id(unique_entity_id)

        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.unique_entity_id, unique_entity_id)

    def test_invalid_cases_for_name_prop(self):
        faker = CategoryFakerBuilder.a_category()

        this = faker.with_invalid_name_none()
        self.assertIsInstance(this, CategoryFakerBuilder)
        name_value = this.name
        self.assertIsNone(name_value)

        this = faker.with_invalid_name_empty()
        self.assertIsInstance(this, CategoryFakerBuilder)
        name_value = this.name
        self.assertEqual(name_value, "")

        this = faker.with_invalid_name_not_a_string()
        self.assertIsInstance(this, CategoryFakerBuilder)
        name_value = this.name
        self.assertEqual(name_value, 123)

        this = faker.with_invalid_name_not_a_string(10)
        self.assertIsInstance(this, CategoryFakerBuilder)
        name_value = this.name
        self.assertEqual(name_value, 10)

        this = faker.with_invalid_name_too_long()
        self.assertIsInstance(this, CategoryFakerBuilder)
        name_value = this.name
        self.assertEqual(len(name_value), 256)

    def test_name_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.name, str)

        this = faker.with_name('Category 1')
        self.assertIsInstance(this, CategoryFakerBuilder)

        self.assertEqual(faker.name, 'Category 1')

    def test_invalid_cases_for_description_prop(self):
        faker = CategoryFakerBuilder.a_category()

        this = faker.with_invalid_description_not_a_string()
        self.assertIsInstance(this, CategoryFakerBuilder)
        description_value = this.description
        self.assertEqual(description_value, 123)

        this = faker.with_invalid_description_not_a_string(10)
        self.assertIsInstance(this, CategoryFakerBuilder)
        description_value = this.description
        self.assertEqual(description_value, 10)

    def test_description_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.description, str)

        this = faker.with_description('Some Description')

        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.description, 'Some Description')

    def test_invalid_cases_for_is_active_prop(self):
        faker = CategoryFakerBuilder.a_category()

        this = faker.with_invalid_is_active_none()
        self.assertIsInstance(this, CategoryFakerBuilder)
        is_active_value = this.is_active
        self.assertIsNone(is_active_value)

        this = faker.with_invalid_is_active_empty()
        self.assertIsInstance(this, CategoryFakerBuilder)
        is_active_value = this.is_active
        self.assertEqual(is_active_value, "")

        this = faker.with_invalid_is_active_not_a_boolean()
        self.assertIsInstance(this, CategoryFakerBuilder)
        is_active_value = this.is_active
        self.assertEqual(is_active_value, 123)

        this = faker.with_invalid_is_active_not_a_boolean(10)
        self.assertIsInstance(this, CategoryFakerBuilder)
        is_active_value = this.is_active
        self.assertEqual(is_active_value, 10)

    def test_is_active_prop(self):
        faker = CategoryFakerBuilder.a_category()
        self.assertIsInstance(faker.is_active, bool)
        self.assertTrue(faker.is_active)

        this = faker.deactivate()

        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertFalse(faker.is_active)

        this = faker.activate()
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertTrue(faker.is_active)

    def test_created_at_throw_exception_when_is_none(self):
        with self.assertRaises(Exception) as assert_error:
            faker = CategoryFakerBuilder.a_category()
            faker.created_at  # pylint: disable=pointless-statement
        self.assertEqual(
            str(assert_error.exception),
            'Prop created_at not have a factory, use "with methods" to set a value'
        )

    def test_created_at_prop(self):
        faker = CategoryFakerBuilder.a_category()
        date = datetime.now()
        this = faker.with_created_at(date)
        self.assertIsInstance(this, CategoryFakerBuilder)
        self.assertEqual(faker.created_at, date)

    def test_build_a_category(self):
        faker = CategoryFakerBuilder.a_category()
        category = faker.build()

        self.assertCategoryPropTypes(category)
        self.assertTrue(category.is_active)

        unique_entity_id = UniqueEntityId()
        date = datetime.now()
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('Category 1')\
            .with_description('Some Description')\
            .deactivate()\
            .with_created_at(date)

        category = builder.build()

        self.assertIsNotNone(category)
        self.assertEqual(category.unique_entity_id, unique_entity_id)
        self.assertEqual(category.name, 'Category 1')
        self.assertEqual(category.description, 'Some Description')
        self.assertFalse(category.is_active)
        self.assertEqual(category.created_at, date)

        category = builder.activate().build()

        self.assertIsNotNone(category)
        self.assertEqual(category.unique_entity_id, unique_entity_id)
        self.assertEqual(category.name, 'Category 1')
        self.assertEqual(category.description, 'Some Description')
        self.assertTrue(category.is_active)
        self.assertEqual(category.created_at, date)

    def test_build_the_categories(self):
        faker = CategoryFakerBuilder.the_categories(2)
        categories = faker.build()

        self.assertIsNotNone(categories)
        self.assertIsInstance(categories, list)
        self.assertEqual(len(categories), 2)

        for category in categories:
            self.assertCategoryPropTypes(category)
            self.assertTrue(category.is_active)

        unique_entity_id = UniqueEntityId()
        date = datetime.now()
        builder = faker.with_unique_entity_id(unique_entity_id)\
            .with_name('Category 1')\
            .with_description('Some Description')\
            .deactivate()\
            .with_created_at(date)

        categories = builder.build()

        for category in categories:
            self.assertIsNotNone(category)
            self.assertEqual(category.unique_entity_id, unique_entity_id)
            self.assertEqual(category.name, 'Category 1')
            self.assertEqual(category.description, 'Some Description')
            self.assertFalse(category.is_active)
            self.assertEqual(category.created_at, date)

        categories = builder.activate().build()
        for category in categories:
            self.assertIsNotNone(category)
            self.assertEqual(category.unique_entity_id, unique_entity_id)
            self.assertEqual(category.name, 'Category 1')
            self.assertEqual(category.description, 'Some Description')
            self.assertTrue(category.is_active)
            self.assertEqual(category.created_at, date)

    def assertCategoryPropTypes(self, category):  # pylint: disable=invalid-name
        self.assertIsNotNone(category)
        self.assertIsInstance(category.unique_entity_id, UniqueEntityId)
        self.assertIsInstance(category.name, str)
        self.assertIsInstance(category.description, str)
        self.assertIsInstance(category.is_active, bool)
        self.assertIsInstance(category.created_at, datetime)
