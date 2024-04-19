''' Unit tests for CategoryInMemoryRepository '''
import datetime
import unittest

from core.category.domain.entities import Category
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository


class TestCategoryInMemoryRepository(unittest.TestCase):
    ''' Test CategoryInMemoryRepository '''
    repo: CategoryInMemoryRepository

    def setUp(self):
        ''' Setup '''
        self.repo = CategoryInMemoryRepository()

    def test_if_no_filter_when_filter_param_is_null(self):
        ''' Test if no filter when filter_param is null '''
        entity = Category(name='test')

        items = [entity]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_filter(items, None)

        self.assertListEqual(items, items_filtered)

    def test_filter(self):
        ''' Test filter '''

        items = [
            Category(name='test'),
            Category(name='TEST'),
            Category(name='other')
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_filter(items, 'TEST')

        self.assertListEqual([items[0], items[1]], items_filtered)

    def test_sort_by_created_at_when_sort_param_is_null(self):
        ''' Test sort by created_at when sort param is null '''

        items = [
            Category(name='test'),
            Category(name='TEST', created_at=datetime.datetime.now(datetime.timezone.utc) +
                    datetime.timedelta(seconds=100)),
            Category(name='other', created_at=datetime.datetime.now(datetime.timezone.utc) +
                    datetime.timedelta(seconds=200)),
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_sort(items, None, None)

        self.assertListEqual([items[2], items[1], items[0]], items_filtered)

    def test_sort_by_name(self):
        ''' Test sort by name '''

        items = [
            Category(name='c'),
            Category(name='b'),
            Category(name='a')
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_sort(items, 'name', 'asc')
        self.assertListEqual([items[2], items[1], items[0]], items_filtered)

        items_filtered = self.repo._apply_sort(items, 'name', 'desc')
        self.assertListEqual([items[0], items[1], items[2]], items_filtered)
