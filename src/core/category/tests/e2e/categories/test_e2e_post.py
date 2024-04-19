import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCategoriesPostE2E:

    def test_post(self):
        client_http = APIClient()
        response: Response = client_http.post(
            '/categories/', data={'name': 'Category 1'})
        assert response.status_code == 201
