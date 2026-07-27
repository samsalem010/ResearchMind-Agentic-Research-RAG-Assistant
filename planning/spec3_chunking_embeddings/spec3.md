# Spec 3: Chunking & Embeddings

## Goal
Process long web documents into semantically meaningful chunks and convert them into mathematical vectors for storage.

## Scope
- Create `Chunk` Pydantic model (`text`, `embedding`, `metadata`).
- Implement `DocumentChunker` using `langchain-text-splitters` (`RecursiveCharacterTextSplitter`) to break `Document` objects into smaller pieces (chunk size ~1000, overlap ~200).
- Implement `OpenAIEmbedder` to connect to OpenAI's `text-embedding-3-small` API, generating 1,536-dimensional vectors for each chunk.
- Add mock tests for both modules.
- *Note: These modules constitute the `process` node in our LangGraph architecture.*
