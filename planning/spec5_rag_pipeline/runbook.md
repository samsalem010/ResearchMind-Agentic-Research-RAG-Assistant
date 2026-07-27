# spec5_rag_pipeline — Runbook

This runbook provides instructions on how to manually verify the RAG Pipeline components.

## Prerequisites

1. Ensure you have activated the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure you have installed the project dependencies:
   ```bash
   pip install -e '.[dev]'
   ```

## Running the Automated Test Suite

Because we extensively mock the OpenAI API and Pinecone interactions, you can verify the logic of the entire pipeline locally without spending any API credits.

```bash
pytest tests/test_pipeline.py -v
```
