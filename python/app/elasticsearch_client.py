# Documentation: https://elasticsearch-py.readthedocs.io/
from elasticsearch import AsyncElasticsearch

"""Elasticsearch client and utilities."""

_DEFAULT_TIMEOUT = 60 * 10


def get_client(request_timeout=_DEFAULT_TIMEOUT):
    url = "http://localhost:5050"
    client = AsyncElasticsearch(url, request_timeout=request_timeout)
    return client
