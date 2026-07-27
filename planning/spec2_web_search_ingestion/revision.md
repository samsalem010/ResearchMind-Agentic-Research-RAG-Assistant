# spec2_web_search_ingestion — Revision Log

This log documents the implementation steps, validation runs, and adjustments made during the Web Search Ingestion milestone.

## Implementation Log (Pivot to SerpApi)

1. **Dependency Addition**: Added `requests` back to `pyproject.toml` to support REST calls to SerpApi. Retained `openai` for downstream embeddings (Spec 3).
2. **Configuration Change**: Updated `config.py` and `.env.example` to require `SERPAPI_API_KEY`.
3. **Search Client Implementation**: Rewrote `WebSearcher` in `src/agentic_research_rag/ingestion/search.py` to use `requests.get` to hit `https://serpapi.com/search`. 
4. **Document Mapping**: The JSON response's `organic_results` array is parsed. `link` maps to `url`, `title` maps to `title`, and `snippet` maps to `content`. We also store the search `position` in the `metadata`.
5. **Mocked Testing**: Updated `tests/test_search.py` to mock `requests.get` returning a fake `organic_results` structure.

## Verification Results

* **Linting & Formatting**: `ruff` fixed long lines successfully.
* **Testing**: `pytest` successfully ran 7 passing tests across the project.

## Revisions and Lessons Learned

* **Modularity Wins**: Because we built our `Document` model as a standardized bridge between ingestion and processing, pivoting the ingestion source (Perplexity -> SerpApi) required zero changes to our downstream Spec 3 pipeline. The `DocumentChunker` simply accepts the shorter snippet Documents from SerpApi instead of the massive Perplexity document, and everything works seamlessly.
