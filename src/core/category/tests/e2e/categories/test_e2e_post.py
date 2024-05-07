from unittest.mock import PropertyMock, patch
from core.category.infra.django_app.serializers import CategorySerializer
import pytest
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from core.category.domain.repositories import CategoryRepository
from core.category.infra.django_app.api import CategoryResource
from core.category.tests.fixture.categories_api_fixture import CreateCategoryApiFixture, HttpExpect
from django_app import container

@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPostE2E:
    client_http: APIClient
    category_repository: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.client_http = APIClient()
        cls.category_repository = container.repository_category_django_orm()

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_invalid_requests())
    def test_invalid_request(self, http_expect: HttpExpect):
        response: Response = self.client_http.post(
            '/categories/', data=http_expect.request.body, format='json')
        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.detail)

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_entity_validation_error())
    def test_entity_validation_error(self, http_expect: HttpExpect):
        with(
            patch.object(CategorySerializer, 'is_valid') as mock_is_valid,
            patch.object(
                CategorySerializer,
                'validated_data',
                new_callable=PropertyMock,
                return_value=http_expect.request.body
            ) as mock_validated_data
        ):
            response = self.client_http.post(
                '/categories/', data=http_expect.request.body, format='json')
            mock_is_valid.assert_called()
            mock_validated_data.assert_called()
            assert response.status_code == 422
            assert response.content == JSONRenderer().render(http_expect.exception.error)

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_save())
    def test_post(self, http_expect: HttpExpect):
        response: Response = self.client_http.post(
            '/categories/', data=http_expect.request.body, format='json')

        assert response.status_code == 201
        assert 'data' in response.data
        data = response.data['data']
        expected_keys = CreateCategoryApiFixture.keys_in_category_response()
        assert list(data.keys()) == expected_keys
        category_created = self.category_repository.find_by_id(data['id'])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.content == JSONRenderer().render(serialized)
        assert response.data == {
            'data': {
                **http_expect.response.body,
                'id': category_created.id,
                'created_at': serialized['data']['created_at'],
            }
        }
        
        