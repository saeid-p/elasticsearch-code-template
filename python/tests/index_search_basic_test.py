from datetime import datetime
import uuid
import pytest  # https://docs.pytest.org/en/7.4.x/
from faker import Faker  # https://pypi.org/project/Faker/
from elasticsearch import Elasticsearch  # https://elasticsearch-py.readthedocs.io/

from ..app import elasticsearch_client

target_index = "test_index_2"


@pytest.fixture
def client():
    client = elasticsearch_client.get_client()
    return client


@pytest.mark.asyncio
async def index_large_dataset_test(client: Elasticsearch):
    get_response = await client.indices.get(index=target_index, ignore_unavailable=True)
    if len(get_response.body) != 0:
        return

    create_response = await client.indices.create(index=target_index)

    assert len(create_response.body) > 0
    assert create_response.body["acknowledged"] == True
    assert create_response.body["index"] == target_index

    fake = Faker()
    for i in range(0, 1000):
        document = {
            "id": str(uuid.uuid4()),
            "seq": i,
            "fullName": fake.name(),
            "address": fake.address(),
            "content": fake.text(),
            "timestamp": datetime.now().isoformat(),
        }

        response = await client.index(
            index=target_index, id=document["id"], document=document
        )

        assert response.body is not None
        assert response.body["result"] in ["created", "updated"]

    client.close()


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


@pytest.mark.asyncio
async def index_search_test(client: Elasticsearch):
    query_size = 20  # The size of the return items.
    from_index = 0
    query = {"match_all": {}}

    response = await client.search(
        index=target_index, query=query, size=query_size, from_=from_index
    )

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


def get_items(response):
    hits = response.body["hits"]
    items = hits["hits"]
    return items


@pytest.mark.asyncio
async def index_search_match_test(client: Elasticsearch):
    # The "match" query searches for documents where the "content" field contains the search term.
    query = {"match": {"content": "Magazine"}}

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0


@pytest.mark.asyncio
async def index_search_must_term_test(client: Elasticsearch):
    """
    "term" query: It is used to search for documents that contain an exact, unanalyzed match of a specified term in a specific field.
        - It's used for searching for exact values, such as keywords, IDs, or other fields where you don't want any text analysis or tokenization to be applied.

    "must" clause:
    - Documents must satisfy the conditions specified in the "must" clause to be considered a match.
    - All "must" clauses must be satisfied for a document to be returned in the search results.
    - "must" clauses are typically used for mandatory criteria that must be present in the documents you want to retrieve.
    """
    query = {
        "bool": {
            "must": [
                # When the mapping for a field indicates that it is of type "text" with a sub-field of type "keyword", it undergoes text analysis.
                # Whoever, the "keyword" sub-field is not analyzed and is suitable for exact matches.
                {"term": {"fullName.keyword": "Thomas Johnson"}},
                {"term": {"seq": 0}},
            ]
        }
    }

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0


@pytest.mark.asyncio
async def index_search_must_match_test(client: Elasticsearch):
    """
    "should" clause:
    - Documents can satisfy the conditions specified in the "should" clause, but they are not required to do so.
    - While documents that meet "should" criteria are given a relevancy boost, failing to meet these criteria does not exclude them from the search results.
    - "should" clauses are often used for optional or desirable criteria that can enhance the relevancy of the documents but are not mandatory.
    """
    query = {
        "bool": {
            "should": [
                # The "match" query searches for documents where the "fullName" field contains the search term.
                {"match": {"fullName": "Thomas"}},
                # The "date_range" query is a specialized version of the "range" query used specifically for date fields.
                {
                    "range": {
                        "timestamp": {
                            # Read more: https://www.elastic.co/guide/en/elasticsearch/reference/8.10/mapping-date-format.html
                            "format": "yyyy-MM-dd",  # ISO with Timezone: date_optional_time
                            "gte": "2022-01-01",
                            "lte": "2022-12-31",
                        }
                    },
                },
            ]
        }
    }

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0


@pytest.mark.asyncio
async def index_search_should_match_test(client: Elasticsearch):
    """
    "should" clause:
    - Documents can satisfy the conditions specified in the "should" clause, but they are not required to do so.
    - While documents that meet "should" criteria are given a relevancy boost, failing to meet these criteria does not exclude them from the search results.
    - "should" clauses are often used for optional or desirable criteria that can enhance the relevancy of the documents but are not mandatory.
    """
    query = {
        "bool": {
            "should": [
                # The "match" query searches for documents where the "fullName" field contains the search term.
                {"match": {"fullName": "Thomas"}},
                # The "range" query is used for numeric or date fields. It allows you to specify a range of values and
                # filter documents where the field falls within that range.
                {"range": {"seq": {"gte": 0, "lte": 30}}},
            ]
        }
    }

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0


@pytest.mark.asyncio
async def index_search_prefix_test(client: Elasticsearch):
    """
    The "prefix" query is used to find documents where the field value starts with the specified prefix.
    This is especially useful for matching partial terms.
    """
    query = {"prefix": {"fullName.keyword": "Thomas"}}

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0


@pytest.mark.asyncio
async def index_search_fuzzy_test(client: Elasticsearch):
    """
    To search for a field with a term and find relevant results, including partial matches like "Magazine"
    when searching for "Magazin," you can use Elasticsearch's "fuzzy" query or "prefix" query.
    """
    query = {"fuzzy": {"content": "Magazin"}}

    response = await client.search(index=target_index, query=query)
    items = get_items(response)
    assert len(items) > 0
