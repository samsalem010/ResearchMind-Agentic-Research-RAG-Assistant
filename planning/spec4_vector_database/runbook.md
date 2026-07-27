# spec4_vector_database — Runbook

This runbook provides instructions on how to manually verify the Pinecone Vector Database integration.

## Prerequisites

1. Ensure you have activated the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure you have installed the project dependencies:
   ```bash
   pip install -e '.[dev]'
   ```
3. Create a Pinecone account at [pinecone.io](https://pinecone.io) and create an index named `agentic-research-index` with dimensions matching your OpenAI embeddings (1536 for `text-embedding-3-small`).
4. Set your Pinecone API key in the `.env` file:
   ```env
   PINECONE_API_KEY=your_actual_key_here
   PINECONE_INDEX_NAME=agentic-research-index
   ```

## Running the Automated Test Suite

Because we mock the Pinecone API, you can run the test suite locally without needing a live API key or an active internet connection.

```bash
pytest tests/test_storage.py -v
```
