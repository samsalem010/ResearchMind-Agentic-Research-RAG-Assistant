# ResearchMind — Agentic Research RAG Assistant

ResearchMind is a state-of-the-art agentic deep research assistant that autonomously investigates topics, compiles findings from the live web, semantically caches results, and presents them in a premium dashboard.

Built using **LangGraph**, **Streamlit**, **Pinecone**, **Instructor**, and **Groq (Llama-3.3-70b)**, it evaluates user intent, identifies information gaps, plans multi-query web searches, and synthesizes comprehensive research reports with inline citations.

---

## 🚀 Key Features

*   **Stateful Orchestration**: Powered by LangGraph to execute an iterative reasoning-action loop.
*   **Semantic Vector Caching**: Interrogates the vector database *first*. If sufficient context exists, it bypasses web search, optimizing API costs and latency.
*   **Targeted Query Planning**: Evaluates retrieved database context for gaps and plans 3-5 distinct search queries specifically targeting those gaps.
*   **Live Web Ingestion**: Integrates with the Perplexity API to fetch real-time, high-fidelity research documents with inline citations.
*   **Structured Outputs**: Utilizes `instructor` to enforce strict Pydantic schema validation on LLM decisions (intent classification, query planning, context evaluation).
*   **RAG vs. Baseline Benchmarking**: Side-by-side comparison of the agent's RAG output against a baseline zero-shot LLM, evaluated across accuracy, depth, and clarity.
*   **Premium Streamlit Dashboard**: Dark-theme web dashboard showing live execution graph tracking, detailed search checklists, and beautiful markdown reports.

---

## 🛠️ Tech Stack

*   **Graph Engine**: [LangGraph](https://github.com/langchain-ai/langgraph)
*   **LLM Provider**: Groq API (`llama-3.3-70b-versatile`)
*   **Embedding Model**: Gemini API (`text-embedding-004`)
*   **Search Engine**: Perplexity API (`sonar` online model)
*   **Vector DB**: Pinecone
*   **Structured Data**: Instructor (Pydantic validation)
*   **Frontend**: Streamlit
*   **Observability**: LangSmith

---

## 📂 Project Structure

```text
agentic-research-rag/
├── app.py                     # Entrypoint for the Streamlit dashboard
├── pyproject.toml             # Python package configuration and dependencies
├── requirements.txt           # Redirects installation to pyproject.toml
├── ARCHITECTURE.md           # Deep-dive system design documentation
├── src/
│   └── agentic_research_rag/
│       ├── config.py          # Configuration loading using Pydantic Settings
│       ├── llm_client.py      # Shared Groq/Gemini API client setup
│       ├── logger.py          # Custom logging configuration
│       ├── agent/
│       │   ├── baseline.py    # Zero-shot baseline LLM model
│       │   ├── graph.py       # LangGraph agent definition & nodes
│       │   ├── nodes.py       # Pydantic schemas and LLM prompt logic
│       │   └── state.py       # Graph state schema (ResearchState)
│       ├── evaluation/
│       │   ├── evaluator.py   # RAG vs Baseline quality evaluation
│       │   └── models.py      # Evaluator Pydantic validation schemas
│       ├── ingestion/
│       │   └── search.py      # Perplexity API web search client
│       ├── pipeline/
│       │   ├── retriever.py   # Vector DB retrieval interface
│       │   └── synthesizer.py # Detailed report synthesizer
│       ├── processing/
│       │   ├── chunking.py    # Text splitter utilities
│       │   ├── embedding.py   # Vector embedding manager
│       │   └── models.py      # Chunk schema
│       └── storage/
│           └── pinecone_db.py # Pinecone vector DB client wrapper
└── tests/                     # 21-test unit suite (fully passing)
```

---

## ⚙️ Setup & Installation

### 1. Prerequisite API Keys
Ensure you have access to the following APIs:
*   **Groq API Key**: For structured reasoning and intent classification.
*   **Gemini API Key**: For text embedding generation (`text-embedding-004`).
*   **Perplexity API Key**: For live web searches.
*   **Pinecone API Key**: For storing vector chunks.

### 2. Environment Configuration
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Fill in your secrets:
```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-research-index
```

### 3. Install Dependencies
Create a virtual environment and install in development/editable mode:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

---

## 🖥️ Running the Application

### Start the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser at [http://localhost:8501](http://localhost:8501).

### Initialize the Vector Index
If you want to manually configure your Pinecone index:
```bash
python scripts/setup_pinecone.py
```

---

## 🧪 Running the Test Suite

Verify that everything is operating correctly:
```bash
pytest
```
*Note: The unit tests use comprehensive patching to simulate external API responses, meaning they run instantly and do not consume API credits.*
