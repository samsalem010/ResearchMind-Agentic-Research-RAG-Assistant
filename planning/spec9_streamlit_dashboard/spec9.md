# Spec 9: Streamlit Dashboard

## Goal
Build a frontend UI for users to seamlessly interact with the Agentic Research RAG system, view its intermediate thinking steps, and consume the final generated reports.

## Scope
- Add `streamlit` to `pyproject.toml` dependencies.
- Expose a generator method (`stream_run`) in the `ResearchAgent` to stream graph node execution states.
- Create an `app.py` root script to host the Streamlit UI.
- Implement an aesthetically pleasing, modern chat/search interface utilizing Streamlit's new features (`st.status`, `st.chat_message`).
- Include an expandable Model Configuration section in the main UI and a sidebar for viewing previously generated `.md` reports.
