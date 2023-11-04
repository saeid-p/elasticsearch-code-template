import { getClient } from "../elasticsearch_client";

const INDEX_NAME = "test_index_2";

describe("Elastic search aggregates.", () => {
  const client = getClient();

  it("Should ping the server.", async () => {
    const response = await client.ping();
    expect(response).toBeTruthy();
  });

  it("Should run a CRUD operation.", async () => {
    const response = await client.ping();
    expect(response).toBeTruthy();
  });

  it("Should return an index document count.", async () => {
    const countResponse = await client.count({
      index: INDEX_NAME,
    });

    expect(countResponse).toBeTruthy();
    expect(countResponse.count).toEqual(1000);
  });
});
