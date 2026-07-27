# Spec 1: Project Foundation

## Goal
Establish a robust, production-ready python project structure that will serve as the foundation for our Agentic Research RAG system.

## Scope
- Initialize a `pyproject.toml` file with essential dependencies (`pydantic`, `python-dotenv`, `openai`, `langchain-text-splitters`, `requests`, `pinecone`, `langgraph`, `instructor`).
- Configure testing (`pytest`) and linting (`ruff`).
- Create a global configuration manager (`src/agentic_research_rag/config.py`) that uses `pydantic-settings` to securely load environment variables (like API keys) from a `.env` file.
- Setup a standardized logging utility (`src/agentic_research_rag/logger.py`).
