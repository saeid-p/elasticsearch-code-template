# Documentation: https://elasticsearch-py.readthedocs.io/
from elasticsearch import AsyncElasticsearch
from . import config

"""Elasticsearch client and utilities."""

HOST: str = config.read("ELASTICSEARCH_HOST")
API_KEY: str = config.read("ELASTICSEARCH_API_KEY")


def get_client():
    client = AsyncElasticsearch(hosts=HOST, api_key=API_KEY, verify_certs=False)
    return client
