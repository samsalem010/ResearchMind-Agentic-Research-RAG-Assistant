# Spec 4: Vector Database

## Goal
Store our embedded research chunks into Pinecone for high-speed, semantic retrieval.

## Scope
- Add `pinecone` (v4+) to project dependencies.
- Implement `PineconeDB` in `src/agentic_research_rag/storage/pinecone_db.py`.
- Create an `upsert` method that packages the `Chunk` embedding and squashes the `Chunk.text` into the Pinecone `metadata` dictionary (as Pinecone only stores vectors and metadata).
- Ensure `upsert` and `search` methods accept a `namespace` argument to isolate data between different research queries.
- Create a `search` method that queries the index with a raw vector and reconstructs `Chunk` objects from the returned matches.
- Create comprehensive mock tests bypassing the real Pinecone network client.
