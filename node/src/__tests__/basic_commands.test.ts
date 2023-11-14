import { getClient } from "../elasticsearch_client";

const TARGET_INDEX = "test_index_1";
const DOC_ID = "7839e7a9-ea50-465b-a346-beddd48be2c8";
const DOC_PAYLOAD = {
  id: DOC_ID,
  fullName: "Kim Scott",
  text: "Elasticsearch: cool. bonsai cool text to analyze and search.",
  timestamp: new Date().toISOString(),
};

describe("Elastic search basic commands.", () => {
  const client = getClient();

  it("Should ping the server.", async () => {
    const response = await client.ping();
    expect(response).toBeTruthy();
  });

  it("Should run a CRUD operation on an index.", async () => {
    const getResponse = await client.indices.get({
      index: TARGET_INDEX,
      ignore_unavailable: true,
    });

    if (getResponse) {
      const deleteResponse = await client.indices.delete({
        index: TARGET_INDEX,
      });
      expect(deleteResponse).toBeTruthy();
    }

    const createResponse = await client.indices.create({
      index: TARGET_INDEX,
    });

    expect(createResponse).toBeTruthy();
    expect(createResponse.acknowledged).toBeTruthy();
    expect(createResponse.index).toEqual(TARGET_INDEX);
  });

  it("Should refresh an index.", async () => {
    const response = await client.indices.refresh({
      index: TARGET_INDEX,
    });

    expect(response).toBeTruthy();
    expect(response._shards).toBeTruthy();
    expect(response._shards.successful).toBeTruthy();
  });

  it("Should write a single document.", async () => {
    const response = await client.index({
      index: TARGET_INDEX,
      id: DOC_ID,
      document: DOC_PAYLOAD,
    });

    expect(response).toBeTruthy();
    const expectedResults = ["created", "updated"];
    expect(expectedResults.includes(response.result)).toBeTruthy();
  });

  it("Should read a single document.", async () => {
    const response = await client.get({
      index: TARGET_INDEX,
      id: DOC_ID,
    });

    expect(response).toBeTruthy();
    expect(response.found).toBeTruthy();
    expect(response._source).toBeTruthy();
  });

  it("Should read the entire content of an index.", async () => {
    const response = await client.search({
      index: TARGET_INDEX,
      query: {
        match_all: {},
      },
    });

    expect(response).toBeTruthy();
    expect(response.hits).toBeTruthy();
    expect(response.hits.total).toEqual({
      relation: "eq",
      value: 1,
    });
  });
});
