# Elasticsearch Code Template & Notes

Elasticsearch provides a wide range of query options to help you search and retrieve documents that match specific criteria. These queries can be categorized into several types based on their functionality. Here are some of the most commonly used query options in Elasticsearch:

- Match Queries:
	- match: Performs full-text search for terms in a specified field.
	- multi_match: Allows searching in multiple fields with a single query.

- Term-Level Queries:
	- term: Searches for documents with an exact match in a specified field.
	- terms: Searches for documents with one or more exact matches in an array field.
	- range: Searches for documents within a specified range of values in a numeric or date field.

- Compound Queries:
	- bool: Combines multiple query clauses with logical operators (e.g., AND, OR, NOT).
	- constant_score: Returns a constant score for all documents matching the query, useful for filtering.
	- function_score: Allows custom scoring functions for documents.

- Full-Text Queries:
	- match_all: Matches all documents.
	- match_phrase: Matches phrases in a specified field.
	- match_phrase_prefix: Matches prefixes of phrases in a specified field.
	- common_terms: Matches common terms while still providing relevant results.
	- query_string: Supports complex query strings with operators.

- Prefix and Wildcard Queries:
	- prefix: Searches for documents where a field starts with a specified prefix.
	- wildcard: Allows wildcard pattern matching in a specified field.
	- regexp: Performs regular expression-based searches.

- Fuzzy Queries:
	- fuzzy: Matches terms with minor typos or variations.
	- fuzzy_like_this: Finds similar documents based on a provided text.

- Geospatial Queries
	- geo_shape: Searches for documents with geospatial shapes.
	- geo_distance: Searches for documents within a specified distance of a point.
	- geo_bounding_box: Filters documents within a specified bounding box.

- Nested Queries:
	- nested: Allows searching within nested objects.

- Script Queries:
	- script: Allows custom scripts to evaluate document matching.

- Date Range Queries:
	- date_range: Searches for documents within a specified date range.

- Span Queries:
	- span_near: Matches documents with spans of terms near each other.
	- span_term: Searches for a single term in a specific span.

- Parent-Child Queries:
	- has_parent: Matches child documents that have a parent matching a query.
	- has_child: Matches parent documents that have a child matching a query.

- Percolator Queries: Used for indexing and matching stored queries against new documents.

- Collapse and Expand Queries:
	- collapse: Allows collapsing similar documents.
	- expand: Expands collapsed documents to show all matching results.
