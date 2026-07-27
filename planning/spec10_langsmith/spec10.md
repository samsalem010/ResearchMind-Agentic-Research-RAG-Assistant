# Spec 10: LangSmith Observability

## Goal
Integrate LangSmith to provide deep tracing, debugging, and observability for the LangGraph agent, its underlying LLM calls, and external tool executions.

## Scope
- Expose LangSmith configuration variables in `.env.example`.
- Ensure `langsmith` is tracked in `pyproject.toml`.
- Use LangSmith wrappers (`wrap_openai`, `wrap_anthropic`) to patch the underlying LLM clients so that all structured outputs (Classification, Planning, Reasoning) and synthesis calls are accurately logged.
- Use LangSmith's `@traceable` decorator to capture latency and parameters for external tool calls (SerpApi searches and Pinecone DB upserts/retrievals).
