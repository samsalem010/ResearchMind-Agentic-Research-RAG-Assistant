# spec4_vector_database — Revision Log

This log documents the implementation steps, validation runs, and adjustments made during the Vector Database milestone.

## Implementation Log

1. **Dependencies**: Added `pinecone` (v9.x) to `pyproject.toml`. 
2. **Configuration**: Added `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` to `config.py` and `.env.example`. Defaults the index name to `agentic-research-index`.
3. **Database Client**: Implemented `PineconeDB` in `src/agentic_research_rag/storage/pinecone_db.py`.
4. **Upsert Logic**: Converts `Chunk` objects into Pinecone vectors. Generates UUIDs for missing IDs. Moves `chunk.text` into the Pinecone `metadata` dictionary so it can be retrieved later. Uploads in batches of 100.
5. **Search Logic**: Queries Pinecone with an embedding vector, parses the returned `matches`, and reconstructs `Chunk` models (extracting `text` back out of the metadata).
6. **Testing**: Implemented `tests/test_storage.py` to heavily mock the `Pinecone` client class, verifying the mapping logic.

## Verification Results

* **Dependency Fix**: The `pinecone-client` package was renamed to `pinecone` by the maintainers. Attempting to run tests with `pinecone-client` threw a hard Exception. We uninstalled it, updated `pyproject.toml` to use `pinecone`, reinstalled, and tests passed.
* **Testing**: `pytest` successfully ran 10 passing tests across the project.

## Revisions and Lessons Learned

* **Metadata Constraints**: Pinecone only accepts strings, numbers, booleans, or lists of strings in its metadata. Because our `Chunk` model holds the raw string `text` separately from the metadata dictionary, we had to temporarily merge `text` into the metadata dictionary before upserting, and `pop` it back out during search retrieval. This pattern works flawlessly.
