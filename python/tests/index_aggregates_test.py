import pytest  # https://docs.pytest.org/en/7.4.x/
from elasticsearch import Elasticsearch  # https://elasticsearch-py.readthedocs.io/

from ..app import elasticsearch_client

target_index = "test_index_2"


@pytest.fixture
def client():
    client = elasticsearch_client.get_client()
    return client


@pytest.mark.asyncio
async def index_document_count_test(client: Elasticsearch):
    index_names = ["test_index_1", "test_index_2"]
    query_size = 0  # Set the result set size to 0 to just get the aggregation results.
    aggs = {"indexes": {"terms": {"field": "_index", "size": len(index_names)}}}

    response = await client.search(
        index=",".join(index_names), aggs=aggs, size=query_size
    )
    aggregations = response.body["aggregations"]
    assert aggregations is not None

    indexes = aggregations["indexes"]
    buckets = indexes["buckets"]
    assert len(buckets) == len(index_names)

    first_bucket = buckets[0]
    assert first_bucket["key"] == index_names[1]
    assert first_bucket["doc_count"] == 1000

    second_bucket = buckets[1]
    assert second_bucket["key"] == index_names[0]
    assert second_bucket["doc_count"] == 1


@pytest.mark.asyncio
async def index_search_test(client: Elasticsearch):
    query_size = 20  # The size of the return items.
    query = {"match_all": {}}

    response = await client.search(index=target_index, query=query, size=query_size)

    assert response.body is not None
    hits = response.body["hits"]
    assert hits is not None

    totals = hits["total"]
    assert totals["value"] == 1000

    items = hits["hits"]
    assert len(items) == query_size

    first_item = items[0]
    first_item_payload = first_item["_source"]
    assert first_item_payload["seq"] == 0
