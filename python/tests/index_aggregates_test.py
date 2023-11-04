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
async def index_aggregate_group_by_term_test(client: Elasticsearch):
    """
    Terms Aggregation - Counting Unique Values.
    Scenario: You want to count the number of documents for each unique value in a specific field,
    such as analyzing the distribution of products in an e-commerce dataset.
    """
    query_size = 0  # The size of the return items.
    aggs = {"group_by_term": {"terms": {"field": "hasFlag"}}}

    response = await client.search(index=target_index, aggs=aggs, size=query_size)

    aggregations = response.body["aggregations"]
    assert aggregations is not None

    indexes = aggregations["group_by_term"]
    buckets = indexes["buckets"]
    assert len(buckets) == 2
    assert buckets[0]["doc_count"] == 666
    assert buckets[1]["doc_count"] == 334


@pytest.mark.asyncio
async def index_aggregate_date_histogram_test(client: Elasticsearch):
    """
    Date Histogram Aggregation - Time Series Analysis.
    Scenario: You have timestamped data, and you want to analyze it over time in intervals (e.g., daily, weekly, or monthly),
    such as tracking the number of orders over time.
    """
    query_size = 0  # The size of the return items.
    aggs = {
        "items_over_time": {
            "date_histogram": {
                "field": "timestamp",
                "calendar_interval": "month",
                "format": "yyyy-MM",
                "min_doc_count": 0,
            }
        }
    }

    response = await client.search(index=target_index, aggs=aggs, size=query_size)
    aggregations = response.body["aggregations"]

    items = aggregations["items_over_time"]
    buckets = items["buckets"]
    assert len(buckets) > 0


@pytest.mark.asyncio
async def index_aggregate_range_test(client: Elasticsearch):
    """
    Range Aggregation - Grouping by Numeric Ranges.
    Scenario: You want to group documents into numeric value ranges to analyze data distribution, such as grouping salaries into income brackets.
    """
    query_size = 0  # The size of the return items.
    aggs = {
        "seq_ranges": {
            "range": {
                "field": "seq",
                "ranges": [
                    {"from": 0, "to": 200},
                    {"from": 200, "to": 600},
                    {"from": 600},
                ],
            }
        }
    }

    response = await client.search(index=target_index, aggs=aggs, size=query_size)
    aggregations = response.body["aggregations"]

    items = aggregations["seq_ranges"]
    buckets = items["buckets"]
    assert len(buckets) > 0
