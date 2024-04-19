''' Input Output DTO '''

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from core.__seedwork.domain.repositories import SearchResult

Filter = TypeVar('Filter')


@dataclass(slots=True, frozen=True)
class SearchInput(Generic[Filter]):
    ''' Search Input DTO '''
    page: Optional[str] = None
    per_page: Optional[str] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None


Item = TypeVar('Item')


@dataclass(slots=True, frozen=True)
class PaginationOutput(Generic[Item]):
    ''' Pagination Output DTO '''
    items: List[Item]
    total: int
    current_page: int
    per_page: int
    last_page: int


Output = TypeVar('Output', bound='PaginationOutput')


@dataclass(slots=True, frozen=True)
class PaginationOutputMapper:
    ''' Pagination Output Mapper '''
    output_child: Output

    @staticmethod
    def from_child(output_child: Output):
        ''' Create PaginationOutputMapper from child '''
        return PaginationOutputMapper(output_child)

    def to_output(self, items: List[Item], result: SearchResult) -> PaginationOutput[Item]:
        ''' Map search result to output '''
        return self.output_child(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page
        )
