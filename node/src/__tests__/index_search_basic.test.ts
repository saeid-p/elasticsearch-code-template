import { v4 as uuidv4 } from "uuid";
import { faker } from "@faker-js/faker";
import { getClient } from "../elasticsearch_client";
import { SearchTotalHits } from "@elastic/elasticsearch/lib/api/types";

const TARGET_INDEX = "test_index_2";

describe("Elastic search basic search.", () => {
  const client = getClient();

  it("Index a large dataset.", async () => {
    const get_response = await client.indices.get({
      index: TARGET_INDEX,
      ignore_unavailable: true,
    });

    if (get_response) return;

    const create_response = await client.indices.create({
      index: TARGET_INDEX,
    });
    expect(create_response).toBeTruthy();
    expect(create_response.acknowledged).toBeTruthy();
    expect(create_response.index).toEqual(TARGET_INDEX);

    const doc_count = 1000;
    const docs = [];

    for (let i = 0; i < doc_count; ++i) {
      const now = new Date();
      now.setDate(now.getDate() - i);
      const doc = {
        id: uuidv4(),
        timestamp: now.toISOString(),
        seq: i,
        fullName: faker.person.fullName(),
        address: faker.location.streetAddress(),
        content: `${faker.commerce.productDescription()}. ${faker.word.words(20)}.`,
        hasFlag: i % 3 == 0,
      };

      docs.push(doc);
    }

    const actions = [];
    docs.forEach((doc) => {
      const action = {
        index: {
          _index: TARGET_INDEX,
        },
      };
      actions.push(action);
      actions.push(doc);
    });

    // https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/bulk_examples.html
    const results = await client.bulk({
      refresh: true,
      operations: actions,
    });

    expect(results.items.length).toEqual(doc_count);
  });

  it("Searching all documents", async () => {
    const results_size = 20;
    const response = await client.search({
      index: TARGET_INDEX,
      query: {
        match_all: {},
      },
      size: results_size,
    });

    expect(response).toBeTruthy();
    const { hits } = response;
    expect(hits).toBeTruthy();

    const { total } = hits;
    expect((total as SearchTotalHits).value > 0).toBeTruthy();

    const { hits: items } = hits;
    expect(items.length).toEqual(results_size);
    const [firstItem] = items;
    expect(firstItem._index).toEqual(TARGET_INDEX);
    expect(firstItem._source).toBeTruthy();
  });

  it("Searching relevancy", async () => {
    const response = await client.search({
      index: TARGET_INDEX,
      query: {
        match: {
          content: "Magazine",
        },
      },
    });

    const total = response.hits.total as SearchTotalHits;
    expect(total.value > 0).toBeTruthy();
  });

  it("Searching with must term", async () => {
    /**
      "term" query: It is used to search for documents that contain an exact, unanalyzed match of a specified term in a specific field.
        - It's used for searching for exact values, such as keywords, IDs, or other fields where you don't want any text analysis or tokenization to be applied.
      "must" clause:
      - Documents must satisfy the conditions specified in the "must" clause to be considered a match.
      - All "must" clauses must be satisfied for a document to be returned in the search results.
      - "must" clauses are typically used for mandatory criteria that must be present in the documents you want to retrieve.
     */
    const response = await client.search({
      index: TARGET_INDEX,
      query: {
        bool: {
          must: [
            // When the mapping for a field indicates that it is of type "text" with a sub-field of type "keyword", it undergoes text analysis.
            // However, the "keyword" sub-field is not analyzed and is suitable for exact matches.
            {
              term: {
                "fullName.keyword": "Brian Schinner",
              },
            },
            {
              range: {
                seq: {
                  gte: 0,
                  lte: 500,
                },
              },
            },
          ],
        },
      },
    });

    const total = response.hits.total as SearchTotalHits;
    expect(total.value > 0).toBeTruthy();
  });

  it("Searching with should match", async () => {
    /**
      "should" clause:
      - Documents can satisfy the conditions specified in the "should" clause, but they are not required to do so.
      - While documents that meet "should" criteria are given a relevancy boost, failing to meet these criteria does not exclude them from the search results.
      - "should" clauses are often used for optional or desirable criteria that can enhance the relevancy of the documents but are not mandatory.
     */
    const response = await client.search({
      index: TARGET_INDEX,
      query: {
        bool: {
          should: [
            // The "match" query searches for documents where the "fullName" field contains the search term.
            {
              match: {
                fullName: "Brian",
              },
            },
            // The "date_range" query is a specialized version of the "range" query used specifically for date fields.
            {
              range: {
                timestamp: {
                  // Read more: https://www.elastic.co/guide/en/elasticsearch/reference/8.10/mapping-date-format.html
                  format: "yyyy-MM-dd", // ISO with Timezone: date_optional_time
                  gte: "2023-01-01",
                  lte: "2023-12-31",
                },
              },
            },
          ],
        },
      },
    });

    const total = response.hits.total as SearchTotalHits;
    expect(total.value > 0).toBeTruthy();
  });

  it("Searching with prefix", async () => {
    /**
      The "prefix" query is used to find documents where the field value starts with the specified prefix.
      This is especially useful for matching partial terms.
     */
    const response = await client.search({
      index: TARGET_INDEX,
      query: { prefix: { "fullName.keyword": "Thomas" } },
    });

    const total = response.hits.total as SearchTotalHits;
    expect(total.value > 0).toBeTruthy();
  });

  it("Searching fuzzy", async () => {
    /**
      To search for a field with a term and find relevant results, including partial matches like "Magazine"
      when searching for "Magazin," you can use Elasticsearch's "fuzzy" query or "prefix" query.
     */
    const response = await client.search({
      index: TARGET_INDEX,
      query: { fuzzy: { content: "Magazin" } },
    });

    const total = response.hits.total as SearchTotalHits;
    expect(total.value > 0).toBeTruthy();
  });
});
