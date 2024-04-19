''' Test RepositoryInterface'''
from dataclasses import dataclass
from typing import Any, List, Optional
import unittest

from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.repositories import (
    ET,
    Filter,
    InMemoryRepository,
    InMemorySearchableRepository,
    RepositoryInterface,
    SearchParams,
    SearchResult,
    SearchableRepositoryInterface
)

from core.__seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):
    ''' Test RepositoryInterface'''

    def test_throw_error_when_methods_not_implemented(self):
        ''' Test RepositoryInterface methods'''
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            RepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class RepositoryInterface with abstract " +
                         "methods delete, find_all, find_by_id, insert, update")


@dataclass(frozen=True, slots=True, kw_only=True)
class StubEntity(Entity):
    '''StubEntity'''
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    '''StubInMemoryRepository'''
    # pylint: disable=unnecessary-pass
    pass


class TestInMemoryRepository(unittest.TestCase):
    ''' Test InMemoryRepository'''

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        ''' Test InMemoryRepository items property'''
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        ''' Test InMemoryRepository insert method'''
        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_not_found_exception_in_find_by_id(self):
        ''' Test InMemoryRepository find_by_id method'''
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('1')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID '1'")

        unique_entity_id = UniqueEntityId(
            'af3e4b3e-0b3d-4b3b-8b3b-3b3b3b3b3b3b')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(assert_error.exception.args[0],
                         "Entity not found using ID 'af3e4b3e-0b3d-4b3b-8b3b-3b3b3b3b3b3b'")

    def test_find_by_id(self):
        ''' Test InMemoryRepository find_by_id method'''
        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        ''' Test InMemoryRepository find_all method'''
        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)

        items = self.repo.find_all()
        self.assertListEqual(items, [entity])

    def test_throw_not_found_exception_in_update(self):
        ''' Test InMemoryRepository update method'''

        entity = StubEntity(name='test', price=1.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'")

    def test_update(self):
        ''' Test InMemoryRepository update method'''
        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            name='test updated',
            price=2.0,
            unique_entity_id=entity.unique_entity_id
        )
        self.repo.update(entity_updated)

        items = self.repo.find_all()
        self.assertListEqual(items, [entity_updated])

    def test_throw_not_found_exception_in_delete(self):
        ''' Test InMemoryRepository delete method'''
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('1')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID '1'")

        unique_entity_id = UniqueEntityId(
            'af3e4b3e-0b3d-4b3b-8b3b-3b3b3b3b3b3b')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(assert_error.exception.args[0],
                         "Entity not found using ID 'af3e4b3e-0b3d-4b3b-8b3b-3b3b3b3b3b3b'")

    def test_delete(self):
        ''' Test InMemoryRepository delete method'''
        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)

        self.repo.delete(entity.id)
        items = self.repo.find_all()
        self.assertListEqual(items, [])

        entity = StubEntity(name='test', price=1.0)
        self.repo.insert(entity)

        self.repo.delete(entity.unique_entity_id)
        items = self.repo.find_all()
        self.assertListEqual(items, [])


class TestSearchableRepositoryInterface(unittest.TestCase):
    ''' Test SearchableRepositoryInterface'''

    def test_throw_error_when_methods_not_implemented(self):
        ''' Test SearchableRepositoryInterface methods'''
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            SearchableRepositoryInterface()
        self.assertEqual(assert_error.exception.args[0],
                         "Can't instantiate abstract class SearchableRepositoryInterface with abstract " +
                         "methods delete, find_all, find_by_id, insert, search, update")

    def test_sortable_fields_prop(self):
        ''' Test SearchableRepositoryInterface sortable_fields property'''
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class TestSearchParams(unittest.TestCase):
    ''' Test SearchParams'''

    def test_props_annotations(self):
        ''' Test SearchParams annotations '''
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter]
        })

    def test_page_prop(self):
        ''' Test SearchParams page prop '''
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': '', 'expected': 1},
            {'page': 'fake', 'expected': 1},
            {'page': '0', 'expected': 1},
            {'page': '-1', 'expected': 1},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
            {'page': 5.5, 'expected': 5},

        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])

    def test_per_page_prop(self):
        ''' Test SearchParams per_page prop '''
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': '', 'expected': 15},
            {'per_page': 'fake', 'expected': 15},
            {'per_page': '0', 'expected': 15},
            {'per_page': '-1', 'expected': 15},
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
            {'per_page': 5.5, 'expected': 5},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'])

    def test_sort_prop(self):
        ''' Test SearchParams sort prop '''
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': '', 'expected': None},
            {'sort': 'fake', 'expected': 'fake'},
            {'sort': '0', 'expected': '0'},
            {'sort': '-1', 'expected': '-1'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': 'False'},
            {'sort': {}, 'expected': '{}'},
            {'sort': 5.5, 'expected': '5.5'},
        ]

        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'])

    def test_sort_dir_prop(self):
        ''' Test SearchParams sort_dir prop '''
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort="")
        self.assertIsNone(params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': 'asc'},
            {'sort_dir': '', 'expected': 'asc'},
            {'sort_dir': 'fake', 'expected': 'asc'},
            {'sort_dir': '0', 'expected': 'asc'},
            {'sort_dir': {}, 'expected': 'asc'},
            {'sort_dir': True, 'expected': 'asc'},
            {'sort_dir': False, 'expected': 'asc'},
            {'sort_dir': 5.5, 'expected': 'asc'},
            {'sort_dir': 'asc', 'expected': 'asc'},
            {'sort_dir': 'ASC', 'expected': 'asc'},
            {'sort_dir': 'desc', 'expected': 'desc'},
            {'sort_dir': 'DESC', 'expected': 'desc'},
        ]

        for i in arrange:
            params = SearchParams(sort='name', sort_dir=i['sort_dir'])
            self.assertEqual(params.sort_dir, i['expected'])

    def test_filter_prop(self):
        ''' Test SearchParams sort prop '''
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {'filter': None, 'expected': None},
            {'filter': '', 'expected': None},
            {'filter': 'fake', 'expected': 'fake'},
            {'filter': '0', 'expected': '0'},
            {'filter': '-1', 'expected': '-1'},
            {'filter': True, 'expected': 'True'},
            {'filter': False, 'expected': 'False'},
            {'filter': {}, 'expected': '{}'},
            {'filter': 5.5, 'expected': '5.5'},
        ]

        for i in arrange:
            params = SearchParams(filter=i['filter'])
            self.assertEqual(params.filter, i['expected'])


class TestSearchResult(unittest.TestCase):
    ''' Test SearchResult'''

    def test_props_annotations(self):
        ''' Test SearchResult annotations '''
        self.assertEqual(SearchResult.__annotations__, {
            'items': List[ET],
            'total': int,
            'current_page': int,
            'per_page': int,
            'last_page': int,
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filter': Optional[Filter]
        })

    def test_constructor(self):
        ''' Test SearchResult constructor '''
        entity = StubEntity(name='test', price=1.0)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2
        )
        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': None,
            'sort_dir': None,
            'filter': None
        })

        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='test'
        )

        self.assertDictEqual(result.to_dict(), {
            'items': [entity, entity],
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 2,
            'sort': 'name',
            'sort_dir': 'asc',
            'filter': 'test'
        })

    def test_when_per_page_is_greater_than_total(self):
        ''' Test SearchResult when per_page is greater than total '''
        result = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=15
        )
        self.assertEqual(result.last_page, 1)

    def test_when_per_page_is_less_than_total_and_they_are_not_multiple(self):
        ''' Test SearchResult when per_page is less than total and they are not multiple '''
        result = SearchResult(
            items=[],
            total=101,
            current_page=1,
            per_page=20
        )
        self.assertEqual(result.last_page, 6)

        result = SearchResult(
            items=[],
            total=100,
            current_page=1,
            per_page=20
        )
        self.assertEqual(result.last_page, 5)


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    '''StubInMemorySearchableRepository'''
    sortable_fields: List[str] = ['name']

    def _apply_filter(self, items: List[StubEntity], filter_param: Any | None) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower()
                                or filter_param == str(i.price), items)
            return list(filter_obj)
        return items


class TestInMemorySearchableRepository(unittest.TestCase):
    ''' Test InMemorySearchableRepository'''

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        ''' Test InMemorySearchableRepository _apply_filter method'''
        items = [StubEntity(name='test', price=1.0)]
        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name='test', price=1.0),
            StubEntity(name='TEST', price=5.0),
            StubEntity(name='fake', price=0)
        ]

        result = self.repo._apply_filter(items, 'TEST')
        self.assertEqual(result, [items[0], items[1]])

        result = self.repo._apply_filter(items, '5.0')
        self.assertEqual(result, [items[1]])

    def test__apply_sort(self):
        ''' Test InMemorySearchableRepository _apply_sort method'''
        items = [
            StubEntity(name='b', price=5.0),
            StubEntity(name='a', price=1.0),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual(result, items)

        # pylint: disable=protected-access
        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual(result, [items[1], items[0]])

        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual(result, items)

        self.repo.sortable_fields.append('price')
        result = self.repo._apply_sort(items, 'price', 'asc')
        self.assertEqual(result, [items[1], items[0]])

        result = self.repo._apply_sort(items, 'price', 'desc')
        self.assertEqual(result, items)

    def test__apply_paginate(self):
        ''' Test InMemorySearchableRepository _apply_paginate method'''
        items = [
            StubEntity(name='b', price=5.0),
            StubEntity(name='a', price=1.0),
            StubEntity(name='c', price=2.0),
            StubEntity(name='d', price=3.0),
            StubEntity(name='e', price=4.0),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_pagination(items, 1, 2)
        self.assertEqual(result, [items[0], items[1]])

        result = self.repo._apply_pagination(items, 2, 2)
        self.assertEqual(result, [items[2], items[3]])

        result = self.repo._apply_pagination(items, 3, 2)
        self.assertEqual(result, [items[4]])

        result = self.repo._apply_pagination(items, 4, 2)
        self.assertEqual(result, [])

    def test_search_when_params_is_empty(self):
        ''' Test InMemorySearchableRepository search method when params is empty'''
        entity = StubEntity(name='test', price=1.0)
        items = [entity] * 16
        self.repo.items = items

        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
            sort=None,
            sort_dir=None,
            filter=None
        ))

    def test_search_applying_filter_and_paginate(self):
        ''' Test InMemorySearchableRepository search method applying filter and paginate'''
        items = [
            StubEntity(name='test', price=1.0),
            StubEntity(name='a', price=0),
            StubEntity(name='TEST', price=5.0),
            StubEntity(name='Test', price=0)
        ]
        self.repo.items = items
        result = self.repo.search(SearchParams(
            filter='TEST', page=1, per_page=2))
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            filter='TEST', page=2, per_page=2))
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
            sort=None,
            sort_dir=None,
            filter='TEST'
        ))

    def test_search_with_sort_and_paginate(self):
        ''' Test InMemorySearchableRepository search method with sort and paginate'''
        items = [
            StubEntity(name='b', price=5.0),
            StubEntity(name='a', price=1.0),
            StubEntity(name='d', price=3.0),
            StubEntity(name='e', price=4.0),
            StubEntity(name='c', price=2.0),
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            sort='name', page=1, per_page=2))

        self.assertEqual(result, SearchResult(
            items=[items[1], items[0]],
            total=5,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter=None
        ))

        result = self.repo.search(SearchParams(
            sort='name', page=2, per_page=2))

        self.assertEqual(result, SearchResult(
            items=[items[4], items[2]],
            total=5,
            current_page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter=None
        ))

        result = self.repo.search(SearchParams(
            sort='name', page=3, per_page=2))

        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=5,
            current_page=3,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter=None
        ))

        arrange = [
            {
                'input': SearchParams(
                    page=1, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=2, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            },
            {
                'input': SearchParams(
                    page=3, per_page=2, sort='name', sort_dir='desc'
                ),
                'output': SearchResult(
                    items=[items[1]],
                    total=5,
                    current_page=3,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                    filter=None
                )
            }
        ]

        for index, item in enumerate(arrange):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                item['output'],
                f"The output using sort_dir desc on index {index} is not the expected")

    def test_search_applying_filter_and_sort_and_pagination(self):
        ''' Test InMemorySearchableRepository search method applying filter, sort and pagination'''
        items = [
            StubEntity(name='test', price=5.0),
            StubEntity(name='a', price=1.0),
            StubEntity(name='TEST', price=5.0),
            StubEntity(name='e', price=4.0),
            StubEntity(name='TeSt', price=0)
        ]
        self.repo.items = items

        result = self.repo.search(SearchParams(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))

        self.assertEqual(result, SearchResult(
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))

        result = self.repo.search(SearchParams(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))

        self.assertEqual(result, SearchResult(
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='TEST'
        ))
