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
    # All crud actions here are idempotent.
    get_response = await client.indices.get(index=target_index, ignore_unavailable=True)

    if len(get_response.body) != 0:
        delete_response = await client.indices.delete(index=target_index)
        assert delete_response.body["acknowledged"] == True

    create_response = await client.indices.create(index=target_index)

    assert len(create_response.body) > 0
    assert create_response.body["acknowledged"] == True
    assert create_response.body["index"] == target_index

    fake = Faker()
    for i in range(0, 1000):
        document = {
            "id": str(uuid.uuid4()),
            "seq": str(i),
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
    assert first_item_payload["seq"] == "0"


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
    assert first_item_payload["seq"] == "0"
