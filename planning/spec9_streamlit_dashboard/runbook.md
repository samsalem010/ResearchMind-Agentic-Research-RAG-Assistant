# spec9_streamlit_dashboard — Runbook

## Setup Requirements
Ensure all API keys are correctly exported in your `.env` file (`OPENAI_API_KEY` and `ANTHROPIC_API_KEY`).

## Running the App
Start the Streamlit development server by running:
```bash
streamlit run app.py
```

Streamlit will automatically open a browser window to `http://localhost:8501`.

Enter a topic in the chat input, and you will see the agent's progress update in real-time as it traverses its reasoning graph, ending with a beautifully rendered markdown report.
