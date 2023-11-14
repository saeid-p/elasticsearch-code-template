// https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/introduction.html
import { Client } from "@elastic/elasticsearch";
import { readEnvironmentVariable } from "./config";

const getClient = () =>
  new Client({
    node: readEnvironmentVariable("ELASTICSEARCH_HOST"),
    requestTimeout: 1 * 60000, // 1min timeout
    auth: {
      apiKey: readEnvironmentVariable("ELASTICSEARCH_API_KEY"),
    },
    tls: {
      // https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/client-connecting.html
      rejectUnauthorized: false,
    },
  });

export { getClient };
