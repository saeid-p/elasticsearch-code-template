from datetime import datetime
import pytest  # https://docs.pytest.org/en/7.4.x/
from elasticsearch import Elasticsearch  # https://elasticsearch-py.readthedocs.io/

from ..app import elasticsearch_client

TARGET_INDEX = "test_index_1"
DOC_ID = "7839e7a9-ea50-465b-a346-beddd48be2c8"
DOC_PAYLOAD = {
    "id": DOC_ID,
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
    get_response = await client.indices.get(index=TARGET_INDEX, ignore_unavailable=True)

    if len(get_response.body) != 0:
        delete_response = await client.indices.delete(index=TARGET_INDEX)
        assert delete_response.body["acknowledged"] == True

    create_response = await client.indices.create(index=TARGET_INDEX)

    assert len(create_response.body) > 0
    assert create_response.body["acknowledged"] == True
    assert create_response.body["index"] == TARGET_INDEX


@pytest.mark.asyncio
async def document_write_single_test(client: Elasticsearch):
    response = await client.index(index=TARGET_INDEX, id=DOC_ID, document=DOC_PAYLOAD)

    assert response.body is not None
    assert response.body["result"] in ["created", "updated"]


@pytest.mark.asyncio
async def document_read_single_test(client: Elasticsearch):
    response = await client.get(index=TARGET_INDEX, id=DOC_ID)

    assert response.body is not None
    assert response.body["found"] == True


@pytest.mark.asyncio
async def index_refresh_by_name_test(client: Elasticsearch):
    response = await client.indices.refresh(index=TARGET_INDEX)

    assert response.body is not None
    assert response.body["_shards"] is not None


@pytest.mark.asyncio
async def index_search_test(client: Elasticsearch):
    query = {"match_all": {}}

    response = await client.search(index=TARGET_INDEX, query=query)

    assert response.body is not None
    hits = response.body["hits"]
    assert hits is not None
    totals = hits["total"]
    assert totals is not None
