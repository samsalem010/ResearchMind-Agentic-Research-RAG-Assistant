# spec12_benchmarking — Runbook

## Usage

To execute the automated benchmarking pipeline, run the following command from the project root:

```bash
python scripts/run_benchmark.py
```

The script will automatically iterate through the predefined dataset of complex queries. For each query, it will:
1. Fire a zero-shot request to the Baseline Agent.
2. Trigger the fully iterative, web-searching LangGraph Agentic RAG pipeline.
3. Pass both answers to the `Evaluator` (GPT-4o) to score based on Comprehensiveness, Recency, Factual Accuracy, and Citations.

Once complete, the script will write a nicely formatted markdown table to `outputs/reports/benchmark_report.md`. You can open this file to review the final verdict.
