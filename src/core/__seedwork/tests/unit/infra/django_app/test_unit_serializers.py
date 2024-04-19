from typing import OrderedDict
import unittest
from rest_framework import serializers

from core.__seedwork.application.dto import PaginationOutput
from core.__seedwork.infra.django_app.serializers import CollectionSerializer, PaginationSerializer, ResourceSerializer


class TestPaginationSerializerUnit(unittest.TestCase):

    def test_serializer(self):
        pagination = {
            'total': '4',
            'current_page': '1',
            'per_page': '2',
            'last_page': '1'

        }
        data = PaginationSerializer(instance=pagination).data

        self.assertEqual(data, {
            'total': 4,
            'current_page': 1,
            'per_page': 2,
            'last_page': 1
        })


class StubSerializer(ResourceSerializer):  # pylint: disable=abstract-method
    name = serializers.CharField()


class StubCollectionSerializer(CollectionSerializer):  # pylint: disable=abstract-method
    child = StubSerializer()


class TestCollectionSerializerUnit(unittest.TestCase):

    def test_if_throw_an_error_when_instance_is_not_a_pagination_output(self):
        error_message = 'instance must be a PaginationOutput'
        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer()
        self.assertEqual(str(assert_error.exception), error_message)
        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer(instance={})
        self.assertEqual(str(assert_error.exception), error_message)
        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer(instance=1)
        self.assertEqual(str(assert_error.exception), error_message)

    def test__init__(self):
        pagination = PaginationOutput(
            items=[1, 2, 3],
            total=4,
            current_page=1,
            per_page=2,
            last_page=1
        )
        collection = StubCollectionSerializer(instance=pagination)
        self.assertEqual(collection.pagination, pagination)
        self.assertFalse(collection.many)
        self.assertEqual(collection.instance, pagination.items)

    def test_serialize(self):
        pagination = PaginationOutput(
            items=[{'name': 'foo'}, {'name': 'bar'}],
            current_page='1',
            per_page='2',
            last_page='3',
            total='4'
        )
        data = StubCollectionSerializer(instance=pagination).data
        self.assertEqual(data, {
            'data': [
                OrderedDict([('name', 'foo')]),
                OrderedDict([('name', 'bar')])
            ],
            'meta': {
                'current_page': 1,
                'per_page': 2,
                'last_page': 3,
                'total': 4
            }
        })
