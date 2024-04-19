
import pytest
from rest_framework.exceptions import ErrorDetail, ValidationError
from django_app import container
from core.__seedwork.infra.testing.helpers import (
    make_request
)
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.infra.django_app.repositories import CategoryDjangoRepository
from core.category.tests.helpers import init_category_resource_all_none
from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import NotFoundException


@pytest.mark.django_db
class TestCategoryResourceDeleteMethodInt:
    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = CategoryDjangoRepository()
        cls.resource = CategoryResource(**{
            **init_category_resource_all_none(),
            'delete_use_case': container.use_case_category_delete_category,
        })

    def test_throw_exception_when_id_is_invalid(self):
        request = make_request(http_method='delete')
        with pytest.raises(ValidationError) as assert_exception:
            self.resource.delete(request, 'invalid id')
        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }

    def test_throw_exception_when_category_not_found(self):
        uuid_value = 'af468b2c-8f4b-4e8d-8e0b-8b4c4a3c1b8c'
        request = make_request(http_method='delete')
        with pytest.raises(NotFoundException) as assert_exception:
            self.resource.delete(request, uuid_value)
        error_message = assert_exception.value.args[0]
        assert error_message == f"Entity not found using ID '{uuid_value}'"

    def test_delete_method(self):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        request = make_request(http_method='delete',)
        response = self.resource.delete(request, category.id)

        assert response.status_code == 204

        with pytest.raises(NotFoundException) as assert_exception:
            self.repo.find_by_id(category.id)
        error_message = assert_exception.value.args[0]
        assert error_message == f"Entity not found using ID '{category.id}'"
