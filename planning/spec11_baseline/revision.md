# spec11_baseline — Revision Log

This log documents the implementation steps for creating a Baseline LLM comparator.

## Implementation Log

1. **Baseline Agent Implementation**: Created `BaselineAgent` in `src/agentic_research_rag/agent/baseline.py`. It initializes a `LangSmith`-wrapped `Anthropic` client and has a simple `run` method that prompts the model directly without tool usage. It utilizes the `Reporter` class to save the output locally as well.
2. **UI Integration**: In `app.py`, added an `st.radio` component to select between "Agentic RAG" and "Baseline LLM". Modified the main chat execution flow to conditionally run the `BaselineAgent` instead of instantiating the LangGraph pipeline.
3. **Testing**: Implemented `tests/test_baseline.py` to assert that the `BaselineAgent` correctly parses prompts and calls the underlying client.

## Verification Results

* **Functional UI**: The Streamlit interface seamlessly swaps modes, allowing side-by-side comparison of results.
* **Testing**: 100% of tests passed, proving the modular integration of the baseline comparator.
