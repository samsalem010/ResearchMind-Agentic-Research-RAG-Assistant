# spec6_langgraph_agent — Runbook

This runbook provides instructions on how to execute the fully assembled LangGraph AI Agent!

## Prerequisites

1. Ensure you have activated the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure you have installed the project dependencies:
   ```bash
   pip install -e '.[dev]'
   ```

## Running the Automated Test Suite

Because we extensively mock all external dependencies, you can run the entire agent workflow locally to verify the state transitions.

```bash
pytest tests/test_agent.py -v
```

## Running the Live Agent (Requires API Keys)

If you are ready to run the agent against live data, you will need to populate your `.env` file with real API keys:

```env
OPENAI_API_KEY=your_real_openai_key
SERPAPI_API_KEY=your_real_serpapi_key
PINECONE_API_KEY=your_real_pinecone_key
PINECONE_INDEX_NAME=agentic-research-index
```

*(Note: Ensure you have created the Pinecone index `agentic-research-index` with a dimension size of `1536` in your Pinecone console).*

Once configured, you can create a simple execution script in the root directory:

```python
# run_agent.py
from agentic_research_rag.agent.graph import ResearchAgent

def main():
    agent = ResearchAgent()
    query = "What are the latest advancements in solid state batteries?"
    
    print(f"Running research agent for: '{query}'\n")
    answer = agent.run(query)
    
    print("\n" + "="*50)
    print("FINAL ANSWER:")
    print("="*50)
    print(answer)

if __name__ == "__main__":
    main()
```

Run it via:
```bash
python run_agent.py
```
