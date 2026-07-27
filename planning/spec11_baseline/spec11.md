# Spec 11: Baseline LLM

## Goal
Establish a simple, non-agentic baseline to compare against our Agentic RAG system. This ensures we can quantitatively and qualitatively prove the value of the LangGraph agent over a standard zero-shot LLM query.

## Scope
- Create `BaselineAgent` in `src/agentic_research_rag/agent/baseline.py`.
- Add a toggle in the Streamlit UI to switch between "Agentic RAG" and "Baseline LLM" modes.
- Implement tests for the `BaselineAgent`.
