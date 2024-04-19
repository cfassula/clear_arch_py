''' Category Repository Interface '''
from abc import ABC
from core.__seedwork.domain.repositories import (
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
    SearchableRepositoryInterface
)
from core.category.domain.entities import Category


class _SearchParams(DefaultSearchParams):
    ''' Category Search Params '''
    # pylint: disable=unnecessary-pass
    pass


class _SearchResult(DefaultSearchResult):
    ''' Category Search Result '''
    # pylint: disable=unnecessary-pass
    pass


class CategoryRepository(
    SearchableRepositoryInterface[Category, _SearchParams, _SearchResult],
    ABC
):
    ''' Category Repository Interface'''

    SearchParams = _SearchParams
    SearchResult = _SearchResult
