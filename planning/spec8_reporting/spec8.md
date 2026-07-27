# Spec 8: Reporting

## Goal
Automatically generate and save formatted Markdown reports based on the agent's findings, providing a persistent record of the research process.

## Scope
- Create a `Reporter` module in `src/agentic_research_rag/reporting/reporter.py`.
- Define a `reports_dir` configuration in `config.py` (default: `outputs/reports`).
- Integrate the `Reporter` into the `ResearchAgent`'s `node_synthesize` step, so that every successful run automatically persists the final answer to disk.
- Include metadata in the report (like the topic and generation timestamp).
