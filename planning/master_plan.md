# Agentic Research RAG — Master Plan

This document tracks the overarching phases and completion status of the Agentic Research RAG project.

## Phases

*   **[x] Spec 1: Project Foundation**
    *   Virtual environment, dependency management (`pyproject.toml`), structured logging, and configuration parsing (`pydantic-settings`).
*   **[x] Spec 2: Web Search Ingestion**
    *   Integration with the Perplexity API (via the OpenAI SDK) to execute web searches and retrieve synthesized research reports with citations. Standardized output using a Pydantic `Document` schema.
*   **[x] Spec 3: Chunking & Embeddings**
    *   Breaking detailed research reports into semantic chunks and generating vector embeddings using OpenAI (`text-embedding-3-small`).
*   **[x] Spec 4: Vector Database**
    *   Storing our embedded research chunks into Pinecone for semantic retrieval.
*   **[x] Spec 5: RAG Pipeline**
    *   Building the retriever to fetch relevant chunks and feed them into a synthesizer LLM.
*   **[x] Spec 6: LangGraph Agent**
    *   Orchestrating the research process using LangGraph to allow the agent to reason, query, and refine its research autonomously.
*   **[x] Spec 7: Multi-LLM**
    *   Introducing support for multiple LLMs for different tasks (e.g., using a smaller model for routing and a larger model for synthesis).
*   **[x] Spec 8: Reporting**
    *   Generating final, formatted markdown or PDF reports based on the agent's findings.
*   **[x] Spec 9: Streamlit Dashboard**
    *   Building a frontend UI for users to interact with the research agent.
*   **[x] Spec 10: LangSmith**
    *   Adding tracing and observability to the LangGraph execution.
*   **[x] Spec 11: Baseline LLM**
    *   Establishing a baseline non-agentic LLM response to compare against our RAG agent.
*   **[x] Spec 12: Benchmarking**
    *   Automated evaluation of the RAG agent's accuracy and depth compared to the baseline.
