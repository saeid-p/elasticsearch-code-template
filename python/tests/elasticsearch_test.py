import pytest
from elasticsearch import Elasticsearch
from ..app import elasticsearch_client


@pytest.fixture
def client():
    client = elasticsearch_client.get_client()
    return client


def read_main_test(client: Elasticsearch):
    assert client is not None
