# Spec 12: Benchmarking

## Goal
Automate the evaluation of the Agentic RAG pipeline by comparing its output against the Baseline LLM using an LLM-as-a-judge mechanism, outputting an objective benchmarking report.

## Scope
- Create `src/agentic_research_rag/evaluation/models.py` with `EvaluationScore` and `ComparisonResult` models.
- Create `src/agentic_research_rag/evaluation/evaluator.py` containing an `Evaluator` class powered by Instructor.
- Create a standalone `scripts/run_benchmark.py` that processes a test dataset of complex topics, runs both agents, and uses the `Evaluator` to grade them side-by-side.
- Ensure the final benchmark writes to `outputs/reports/benchmark_report.md`.
