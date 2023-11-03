from datetime import datetime
import pytest  # https://docs.pytest.org/en/7.4.x/
from elasticsearch import Elasticsearch  # https://elasticsearch-py.readthedocs.io/

from ..app import elasticsearch_client

target_index = "test_index_1"
document_id = "7839e7a9-ea50-465b-a346-beddd48be2c8"
document_payload = {
    "id": document_id,
    "fullName": "Kim Scott",
    "text": "Elasticsearch: cool. bonsai cool text to analyze and search.",
    "timestamp": datetime.now().isoformat(),
}


@pytest.fixture
def client():
    client = elasticsearch_client.get_client()
    return client


@pytest.mark.asyncio
async def client_ping_test(client: Elasticsearch):
    response = await client.ping()
    assert response == True


@pytest.mark.asyncio
async def index_crud_test(client: Elasticsearch):
    # All crud actions here are idempotent.
    get_response = await client.indices.get(index=target_index, ignore_unavailable=True)

    if len(get_response.body) != 0:
        delete_response = await client.indices.delete(index=target_index)
        assert delete_response.body["acknowledged"] == True

    create_response = await client.indices.create(index=target_index)

    assert len(create_response.body) > 0
    assert create_response.body["acknowledged"] == True
    assert create_response.body["index"] == target_index


@pytest.mark.asyncio
async def document_write_single_test(client: Elasticsearch):
    response = await client.index(
        index=target_index, id=document_id, document=document_payload
    )

    assert response.body is not None
    assert response.body["result"] in ["created", "updated"]


@pytest.mark.asyncio
async def document_read_single_test(client: Elasticsearch):
    response = await client.get(index=target_index, id=document_id)

    assert response.body is not None
    assert response.body["found"] == True


@pytest.mark.asyncio
async def index_refresh_by_name_test(client: Elasticsearch):
    response = await client.indices.refresh(index=target_index)

    assert response.body is not None
    assert response.body["_shards"] is not None


@pytest.mark.asyncio
async def index_search_test(client: Elasticsearch):
    query = {"match_all": {}}

    response = await client.search(index=target_index, query=query)

    assert response.body is not None
    hits = response.body["hits"]
    assert hits is not None
    totals = hits["total"]
    assert totals is not None
