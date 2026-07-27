# spec3_chunking_embeddings — Revision Log

This log documents the implementation steps, validation runs, and adjustments made during the Chunking and Embeddings milestone.

## Implementation Log

1. **Prompt Engineering**: Tweaked the Perplexity system prompt in `search.py` to request deep, exhaustive research to ensure we have enough data to chunk.
2. **Chunking**: Added `langchain-text-splitters` to `pyproject.toml`. Implemented `DocumentChunker` using the recursive character text splitter. This ensures chunks don't cut off mid-word or mid-sentence.
3. **Data Model**: Introduced the `Chunk` Pydantic model (`text`, `embedding`, `metadata`) in `src/agentic_research_rag/processing/models.py`.
4. **Embeddings**: Implemented `OpenAIEmbedder` in `src/agentic_research_rag/processing/embedding.py` using `text-embedding-3-small`. Batch processing is supported natively by the SDK.
5. **Testing**: Implemented `tests/test_processing.py` to mock the OpenAI API and verify chunk generation.

## Verification Results

* **Linting & Formatting**: `ruff` fixed long lines successfully.
* **Testing**: `pytest` successfully ran all 7 passing tests across the project.

## Revisions and Lessons Learned

* **Metadata Inheritance**: When chunking, we need to ensure that the metadata from the parent `Document` (specifically the citations and source URLs) is copied down into the `metadata` dictionary of every child `Chunk`. This was successfully implemented in the `DocumentChunker` loop, guaranteeing we don't lose citation context when we embed the text.
