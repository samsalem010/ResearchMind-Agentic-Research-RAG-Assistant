# Spec 2: Web Search Ingestion (SerpApi Pivot)

## Goal
Enable the agent to search the web and retrieve textual snippets from web pages using SerpApi.

## Scope
- Define a strict `Document` Pydantic model (`url`, `title`, `content`, `metadata`).
- Create `WebSearcher` in the `ingestion` module to interface with SerpApi's JSON REST endpoint using the `requests` library.
- Map the Google `snippet` (from SerpApi) to the `content` field.
- Create unit tests that mock `requests.get` to validate data transformation without hitting the network.
- *Note: This module is used extensively by the LangGraph `search` node, which iterates over multiple LLM-planned queries.*
