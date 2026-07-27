# spec6_langgraph_agent — Revision Log

This log documents the implementation steps, validation runs, and adjustments made during the LangGraph Agent Orchestration milestone.

## Implementation Log

1. **Dependency Injection**: Added `langgraph` and `instructor` to `pyproject.toml`.
2. **State Definition**: Defined `ResearchState` in `src/agentic_research_rag/agent/state.py` tracking iterative data.
3. **Instructor Nodes**: Created `AgentNodes` in `src/agentic_research_rag/agent/nodes.py` returning Pydantic schemas (`IntentClassification`, `QueryPlan`, `ReasoningEvaluation`) to guarantee deterministic routing variables.
4. **Graph Construction (Semantic Cache)**: Implemented `ResearchAgent` in `src/agentic_research_rag/agent/graph.py`. 
    *   Wired a loop that checks the database *first*. If the DB context satisfies the prompt, it goes straight to synthesis, bypassing costly web searches.
    *   If gaps exist, it plans 3-5 queries targeting the gaps, searches the web, processes the chunks into Pinecone, and loops back (max 3 iterations).
5. **Testing**: Implemented `tests/test_agent.py` with 16 total project tests. Verified cache hit routing (skipping search) and non-research rejection.

## Verification Results

* **Testing**: `pytest` successfully ran 16 passing tests across the project.

## Revisions and Lessons Learned

* **Pydantic + Instructor**: Relying on standard LLM string parsing for routing (e.g., "return YES or NO") is brittle. `instructor` forcing strict JSON schema evaluation makes complex graph routing perfectly stable.
* **Semantic Caching**: By simply rearranging the LangGraph edges (`classify` -> `retrieve` -> `reason`), we achieved a massive performance optimization without writing any new caching logic. The Vector DB naturally acts as our cache.
