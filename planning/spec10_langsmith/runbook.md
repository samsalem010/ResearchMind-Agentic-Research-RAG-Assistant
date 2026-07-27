# spec10_langsmith — Runbook

## Setup Requirements
Ensure your `.env` file contains the required LangSmith configuration:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=agentic-research-rag
```

## Validation
Once configured, run the Streamlit app:
```bash
streamlit run app.py
```
Execute a search query. Then, open your browser and navigate to [smith.langchain.com](https://smith.langchain.com/). 
You should see a new project named `agentic-research-rag` containing a beautiful, nested trace tree of your LangGraph execution!
