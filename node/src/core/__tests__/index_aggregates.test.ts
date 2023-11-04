import { getClient } from "../elasticsearch_client";

const TARGET_INDEX = "test_index_2";

describe("Elastic search aggregates.", () => {
  const client = getClient();

  it("Count document count in multiple indexes", async () => {
    const indexNames = ["test_index_1", "test_index_2"];
    const querySize = 0; // Set the result set size to 0 to just get the aggregation results.
    const response = await client.search({
      index: indexNames.join(","),
      aggs: {
        indexes: {
          terms: {
            field: "_index",
            size: indexNames.length,
          },
        },
      },
      size: querySize,
    });

    const { aggregations } = response;
    const { indexes } = aggregations;
    const buckets = indexes["buckets"];
    expect(buckets.length === 2).toBeTruthy();

    const [bucket1, bucket2] = buckets;
    expect(bucket1["doc_count"] > 0).toBeTruthy();
    expect(bucket2["doc_count"] > 0).toBeTruthy();
  });

  it("Aggregate group by term", async () => {
    /**
      Terms Aggregation - Counting Unique Values.
      Scenario: You want to count the number of documents for each unique value in a specific field,
      such as analyzing the distribution of products in an e-commerce dataset.
     */
    const querySize = 0;
    const response = await client.search({
      index: TARGET_INDEX,
      aggs: {
        group_by_term: {
          terms: {
            field: "hasFlag",
          },
        },
      },
      size: querySize,
    });

    const { aggregations } = response;
    const items = aggregations["group_by_term"];
    const buckets = items["buckets"];
    expect(buckets.length === 2).toBeTruthy();

    const [bucket1, bucket2] = buckets;
    expect(bucket1["doc_count"] > 0).toBeTruthy();
    expect(bucket2["doc_count"] > 0).toBeTruthy();
  });

  it("Aggregate date histogram", async () => {
    /**
      Date Histogram Aggregation - Time Series Analysis.
      Scenario: You have timestamped data, and you want to analyze it over time in intervals (e.g., daily, weekly, or monthly),
      such as tracking the number of orders over time.
     */
    const querySize = 0;
    const response = await client.search({
      index: TARGET_INDEX,
      aggs: {
        items_over_time: {
          date_histogram: {
            field: "timestamp",
            calendar_interval: "month",
            format: "yyyy-MM",
            min_doc_count: 0,
          },
        },
      },
      size: querySize,
    });

    const { aggregations } = response;
    const items = aggregations["items_over_time"];
    const buckets = items["buckets"];
    expect(buckets.length > 0).toBeTruthy();
  });

  it("Aggregate range", async () => {
    /**
      Range Aggregation - Grouping by Numeric Ranges.
      Scenario: You want to group documents into numeric value ranges to analyze data distribution, such as grouping salaries into income brackets.
     */
    const querySize = 0;
    const response = await client.search({
      index: TARGET_INDEX,
      aggs: {
        seq_ranges: {
          range: {
            field: "seq",
            ranges: [{ from: 0, to: 200 }, { from: 200, to: 600 }, { from: 600 }],
          },
        },
      },
      size: querySize,
    });

    const { aggregations } = response;
    const items = aggregations["seq_ranges"];
    const buckets = items["buckets"];
    expect(buckets.length > 0).toBeTruthy();
  });
});
