# spec2_web_search_ingestion — Runbook

This runbook provides instructions on how to manually execute and verify the Web Search Ingestion feature using SerpApi.

## Prerequisites

1. Ensure you have activated the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Ensure you have installed the project dependencies:
   ```bash
   pip install -e '.[dev]'
   ```
3. Set your SerpApi API key in the `.env` file (or export it in your shell):
   ```env
   SERPAPI_API_KEY=your_actual_key_here
   ```

## Manual Verification (Scratch Script)

To see the `WebSearcher` in action against the live SerpApi endpoint, you can run a quick scratch script.

1. Create a file named `scratch_search.py` in the root of the project:
   ```python
   from agentic_research_rag.ingestion.search import WebSearcher
   from agentic_research_rag.logger import logger

   def main():
       # Initialize the searcher (it automatically picks up SERPAPI_API_KEY from .env)
       try:
           searcher = WebSearcher()
       except ValueError as e:
           logger.error(f"Setup Error: {e}")
           return

       query = "Latest AI trends 2024"
       logger.info(f"Starting test search for: {query}")
       
       # Execute the search
       docs = searcher.search(query, max_results=3)
       
       # Print the results
       for doc in docs:
           print("\n" + "="*50)
           print(f"TITLE: {doc.title}")
           print(f"URL: {doc.url}")
           print(f"POSITION: {doc.metadata.get('position')}")
           print("="*50)
           print(f"SNIPPET:\n{doc.content}\n")

   if __name__ == "__main__":
       main()
   ```

2. Execute the script:
   ```bash
   python scratch_search.py
   ```

## Running the Automated Test Suite

To run the unit tests (which mock SerpApi to avoid network delays and costs):
```bash
pytest tests/test_search.py -v
```
