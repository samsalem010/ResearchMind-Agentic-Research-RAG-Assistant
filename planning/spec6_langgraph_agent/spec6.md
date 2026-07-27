# Spec 6: LangGraph Agent Orchestration (Iterative Research Loop)

## Goal
Connect all individual RAG components (Specs 2-5) into a dynamic, semantic, iterative reasoning agent using LangGraph and Instructor.

## Scope
- Define `ResearchState` using `TypedDict` to track `topic`, `is_research`, `iteration`, `planned_queries`, `reasoning_gaps`, `documents`, `retrieved_chunks`, and `final_answer`.
- Use `instructor` to enforce strictly typed Pydantic models on OpenAI responses for LLM logic nodes.
- Build three LLM reasoning nodes in `agent/nodes.py`:
  1. `classify_intent`: Rejects non-research tasks (commands, coding, writing) to keep the agent focused.
  2. `plan_queries`: Generates 3-5 diverse search queries, targeting specific gaps if looping.
  3. `reason_about_context`: Evaluates if the DB context is sufficient to answer the topic.
- Build a semantic cache DAG in `agent/graph.py`:
  - `classify` -> if not research -> `END`
  - `classify` -> if research -> `retrieve` (Semantic Cache DB hit)
  - `retrieve` -> `reason` -> if no gaps -> `synthesize` -> `END` (Cache success bypass)
  - `reason` -> if gaps -> `plan` -> `search` -> `process` -> loop back to `retrieve`
- Add complex unit tests in `test_agent.py` mocking Instructor responses and verifying short-circuit cache routing.
