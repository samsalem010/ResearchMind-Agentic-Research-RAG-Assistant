import os
import time
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from agentic_research_rag.agent.graph import ResearchAgent
from agentic_research_rag.agent.baseline import BaselineAgent
from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.processing.chunking import DocumentChunker

# Load environment variables
load_dotenv()

# Set up page configuration
st.set_page_config(
    page_title="Research Assistant — AI-Powered Deep Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# Premium CSS: Glassmorphism dark theme with animated accents
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: rgba(17, 24, 39, 0.7);
        --bg-glass: rgba(255, 255, 255, 0.03);
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-glow: rgba(99, 102, 241, 0.3);
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-indigo: #818cf8;
        --accent-violet: #a78bfa;
        --accent-cyan: #22d3ee;
        --accent-emerald: #34d399;
        --accent-amber: #fbbf24;
        --accent-rose: #fb7185;
        --gradient-brand: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #22d3ee 100%);
        --gradient-card: linear-gradient(145deg, rgba(129,140,248,0.08), rgba(34,211,238,0.04));
        --shadow-glow: 0 0 30px rgba(129, 140, 248, 0.08);
    }

    /* ── Base Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    /* Streamlit default overrides */
    .stApp header { background: transparent !important; }
    h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; font-family: 'Inter', sans-serif !important; }
    p, span, li, div { font-family: 'Inter', sans-serif !important; }
    .stMarkdown p { color: var(--text-secondary); }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1729 0%, #111827 100%) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
    }

    /* ── Brand Header ── */
    .brand-header {
        padding: 0.5rem 0 1rem 0;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 1.2rem;
    }
    .brand-logo {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: var(--gradient-brand);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.15rem;
    }
    .brand-tagline {
        font-size: 0.72rem;
        color: var(--text-muted);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* ── Sidebar Environment Cards ── */
    .env-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    .env-card:hover {
        border-color: var(--border-glow);
        background: rgba(129, 140, 248, 0.04);
    }
    .env-label {
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        margin-bottom: 0.15rem;
    }
    .env-val {
        font-size: 0.82rem;
        color: var(--text-primary);
        font-weight: 600;
    }

    /* ── History Items ── */
    .history-item {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.5rem 0.7rem;
        margin-bottom: 0.4rem;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    .history-item:hover {
        background: rgba(129, 140, 248, 0.06);
        border-color: var(--border-glow);
        color: var(--text-primary);
    }

    /* ── Hero Section ── */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }
    .hero-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: var(--gradient-brand);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.6rem;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    /* ── Workflow Cards ── */
    .workflow-card {
        background: var(--gradient-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.6rem 1.4rem;
        text-align: center;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .workflow-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-brand);
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .workflow-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-4px);
        box-shadow: var(--shadow-glow);
    }
    .workflow-card:hover::before {
        opacity: 1;
    }
    .workflow-card-icon {
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .workflow-card h3 {
        color: var(--text-primary) !important;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0.3rem 0 0.5rem 0;
        letter-spacing: -0.01em;
    }
    .workflow-card p {
        color: var(--text-secondary) !important;
        font-size: 0.82rem;
        line-height: 1.5;
        flex-grow: 1;
    }

    /* ── Feature Pills (Landing) ── */
    .feature-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-bottom: 2.5rem;
    }
    .pill {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 100px;
        padding: 0.35rem 0.9rem;
        font-size: 0.72rem;
        color: var(--text-secondary);
        font-weight: 500;
        letter-spacing: 0.02em;
    }

    /* ── Breadcrumb ── */
    .breadcrumb {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .breadcrumb-active {
        color: var(--accent-indigo);
        font-weight: 600;
    }

    /* ── Metric Cards ── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.6rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .metric-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease;
    }
    .metric-card:hover {
        border-color: var(--border-glow);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: var(--gradient-brand);
        opacity: 0.4;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        background: var(--gradient-brand);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        margin-top: 0.2rem;
    }

    /* ── Pipeline Step Indicators ── */
    .pipeline-container {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    .pipeline-step {
        display: flex;
        align-items: center;
        padding: 0.45rem 0.5rem;
        margin-bottom: 0.3rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        font-size: 0.83rem;
    }
    .pipeline-step:last-child { margin-bottom: 0; }
    .step-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.7rem;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }
    .step-completed .step-dot {
        background: var(--accent-emerald);
        box-shadow: 0 0 8px rgba(52, 211, 153, 0.5);
    }
    .step-completed .step-label { color: var(--accent-emerald); font-weight: 500; }
    .step-cached .step-dot {
        background: var(--accent-cyan);
        box-shadow: 0 0 8px rgba(34, 211, 238, 0.4);
    }
    .step-cached .step-label { color: var(--accent-cyan); font-weight: 500; }
    .step-active .step-dot {
        background: var(--accent-amber);
        box-shadow: 0 0 8px rgba(251, 191, 36, 0.5);
        animation: pulse-dot 1.5s infinite;
    }
    .step-active .step-label { color: var(--accent-amber); font-weight: 500; }
    @keyframes pulse-dot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.6); opacity: 0.6; }
    }
    .step-pending .step-dot { background: var(--text-muted); opacity: 0.3; }
    .step-pending .step-label { color: var(--text-muted); }
    .step-label { font-size: 0.82rem; }
    .step-suffix { font-size: 0.7rem; color: var(--text-muted); margin-left: 0.3rem; }

    /* ── Document Stream ── */
    .doc-stream {
        max-height: 420px;
        overflow-y: auto;
        padding-right: 0.3rem;
    }
    .doc-stream::-webkit-scrollbar { width: 4px; }
    .doc-stream::-webkit-scrollbar-track { background: transparent; }
    .doc-stream::-webkit-scrollbar-thumb { background: var(--border-subtle); border-radius: 4px; }

    .doc-entry {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-left: 3px solid var(--accent-indigo);
        padding: 0.7rem 0.8rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .doc-entry:hover {
        border-left-color: var(--accent-cyan);
        background: rgba(129, 140, 248, 0.04);
    }
    .doc-entry-title {
        font-weight: 600;
        font-size: 0.82rem;
        color: var(--text-primary);
        margin-bottom: 0.2rem;
        line-height: 1.3;
    }
    .doc-entry-url {
        font-size: 0.72rem;
        color: var(--accent-indigo);
        text-decoration: none;
        opacity: 0.8;
    }
    .doc-entry-url:hover { opacity: 1; text-decoration: underline; }

    /* ── Report Card ── */
    .report-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        padding: 2rem;
        border-radius: 16px;
        margin-top: 1rem;
        color: var(--text-primary);
        line-height: 1.7;
        position: relative;
    }
    .report-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--gradient-brand);
        border-radius: 16px 16px 0 0;
    }
    .report-card h1, .report-card h2, .report-card h3 {
        color: var(--text-primary) !important;
    }
    .report-card p { color: var(--text-secondary) !important; }
    .report-card a { color: var(--accent-indigo) !important; }
    .report-card strong { color: var(--text-primary) !important; }

    /* ── Comparison View ── */
    .comparison-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .comparison-badge {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
    }
    .badge-baseline {
        background: rgba(251, 113, 133, 0.15);
        color: var(--accent-rose);
        border: 1px solid rgba(251, 113, 133, 0.2);
    }
    .badge-rag {
        background: rgba(52, 211, 153, 0.15);
        color: var(--accent-emerald);
        border: 1px solid rgba(52, 211, 153, 0.2);
    }

    /* ── Metrics Bar (Comparison) ── */
    .metrics-bar {
        display: flex;
        gap: 1rem;
        font-size: 0.78rem;
        color: var(--text-secondary);
        margin-bottom: 0.8rem;
        flex-wrap: wrap;
    }
    .metrics-bar span { font-weight: 600; color: var(--text-primary); }

    /* ── Section Divider ── */
    .section-divider {
        height: 1px;
        background: var(--border-subtle);
        margin: 1.5rem 0;
    }

    /* ── Section Label ── */
    .section-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    /* ── Buttons ── */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background: var(--gradient-brand) !important;
        border: none !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 20px rgba(129, 140, 248, 0.3) !important;
    }
    .stButton > button[kind="secondary"],
    .stDownloadButton > button[kind="secondary"] {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stDownloadButton > button[kind="secondary"]:hover,
    .stButton > button[kind="secondary"]:active,
    .stDownloadButton > button[kind="secondary"]:active,
    .stButton > button[kind="secondary"]:focus,
    .stDownloadButton > button[kind="secondary"]:focus {
        background: rgba(129, 140, 248, 0.1) !important;
        border-color: var(--border-glow) !important;
        color: var(--accent-indigo) !important;
    }

    /* ── Status Widget ── */
    [data-testid="stStatusWidget"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
    }
    [data-testid="stStatusWidget"] label {
        color: var(--text-primary) !important;
    }
    [data-testid="stStatusWidget"] [data-testid="stExpanderDetails"] {
        background-color: transparent !important;
        color: var(--text-secondary) !important;
    }
    /* Fix weird white background issues on status header */
    [data-testid="stStatusWidget"] summary {
        background-color: transparent !important;
    }

    /* ── Text Input ── */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput input::placeholder {
        color: #6b7280 !important;
    }
    .stTextInput input:focus {
        border-color: var(--accent-indigo) !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.15) !important;
    }

    /* Hide streamlit footer and menu */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "mode" not in st.session_state:
    st.session_state.mode = None
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "current_run" not in st.session_state:
    st.session_state.current_run = None

def clear_run_state():
    st.session_state.is_running = False
    st.session_state.current_run = None

def reset_to_landing():
    st.session_state.mode = None
    clear_run_state()

# ─────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">🔬 Research Assistant</div>
        <div class="brand-tagline">AI-Powered Deep Research Engine</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✦  New Research", use_container_width=True):
        reset_to_landing()
        st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Environment Details
    st.markdown('<div class="section-label">Tech Stack</div>', unsafe_allow_html=True)

    from agentic_research_rag.processing.embedding import GeminiEmbedder
    emb_prov = GeminiEmbedder.MODEL_LABEL

    st.markdown(f"""
    <div class="env-card">
        <div class="env-label">Reasoning LLM</div>
        <div class="env-val">Llama 3.3 70B · Groq</div>
    </div>
    <div class="env-card">
        <div class="env-label">Web Search</div>
        <div class="env-val">Perplexity Sonar</div>
    </div>
    <div class="env-card">
        <div class="env-label">Embeddings</div>
        <div class="env-val">{emb_prov}</div>
    </div>
    <div class="env-card">
        <div class="env-label">Vector Store</div>
        <div class="env-val">Pinecone Serverless</div>
    </div>
    <div class="env-card">
        <div class="env-label">Orchestration</div>
        <div class="env-val">LangGraph</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Research History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history):
            mode_icons = {"knowledge_base": "📦", "agentic_rag": "🔬", "compare": "⚖️"}
            icon = mode_icons.get(item["mode"], "📄")
            if st.button(f"{icon}  {item['topic'][:25]}…", key=f"hist_{idx}", use_container_width=True):
                st.session_state.mode = item["mode"]
                st.session_state.current_run = item
                st.session_state.is_running = False
                st.rerun()
    else:
        st.caption("No research sessions yet.")

# ─────────────────────────────────────────────────────────
# Helper: Render Pipeline Steps
# ─────────────────────────────────────────────────────────
def render_pipeline(checklist: dict, progress: int) -> str:
    html = '<div class="pipeline-container">'
    for step, status in checklist.items():
        css_class = "step-pending"
        suffix = ""
        if status == "completed":
            css_class = "step-completed"
        elif status == "cached":
            css_class = "step-cached"
            suffix = '<span class="step-suffix">cached</span>'
        elif status == "pending" and progress > 0:
            css_class = "step-active"
        html += f'<div class="pipeline-step {css_class}"><span class="step-dot"></span><span class="step-label">{step}</span>{suffix}</div>'
    html += '</div>'
    return html

def render_metrics(metrics: dict) -> str:
    return f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value">{metrics["sources"]}</div>
            <div class="metric-label">Citations</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics["documents"]}</div>
            <div class="metric-label">Documents</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics["chunks"]}</div>
            <div class="metric-label">Chunks</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{metrics["embeddings"]}</div>
            <div class="metric-label">Embeddings</div>
        </div>
    </div>
    """

def render_docs(documents: list) -> str:
    html = '<div class="doc-stream">'
    if documents:
        for doc in documents:
            title = doc["title"] or "Search Report"
            url = doc["url"] or "#"
            html += f'<div class="doc-entry"><div class="doc-entry-title">{title}</div><a class="doc-entry-url" href="{url}" target="_blank">{url[:65]}…</a></div>'
    else:
        html += '<p style="color: var(--text-muted); font-size: 0.82rem; padding: 0.5rem;">Awaiting search results…</p>'
    html += '</div>'
    return html

# ─────────────────────────────────────────────────────────
# Main Landing Screen
# ─────────────────────────────────────────────────────────
if st.session_state.mode is None:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">🔬</div>
        <div class="hero-title">Research Assistant</div>
        <div class="hero-subtitle">
            Harness agentic AI to search the web, reason over sources,
            and synthesize publication-ready research reports — in seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature pills
    st.markdown("""
    <div class="feature-pills">
        <span class="pill">🧠 Intent Classification</span>
        <span class="pill">🔍 Multi-Query Search</span>
        <span class="pill">📊 RAG Retrieval</span>
        <span class="pill">🔄 Reasoning Loops</span>
        <span class="pill">📦 Vector Caching</span>
        <span class="pill">⚖️ Baseline Comparison</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="workflow-card">
            <div>
                <div class="workflow-card-icon">📦</div>
                <h3>Build Knowledge Base</h3>
                <p>Search the web, extract content, generate semantic embeddings, and populate your Pinecone vector store for future retrieval.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Builder", key="btn_kb", use_container_width=True, type="primary"):
            st.session_state.mode = "knowledge_base"
            clear_run_state()
            st.rerun()

    with col2:
        st.markdown("""
        <div class="workflow-card">
            <div>
                <div class="workflow-card-icon">🔬</div>
                <h3>Agentic RAG Research</h3>
                <p>Execute an iterative LangGraph workflow with intent parsing, query planning, retrieval, gap analysis, and final synthesis.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Agent", key="btn_rag", use_container_width=True, type="primary"):
            st.session_state.mode = "agentic_rag"
            clear_run_state()
            st.rerun()

    with col3:
        st.markdown("""
        <div class="workflow-card">
            <div>
                <div class="workflow-card-icon">⚖️</div>
                <h3>RAG vs Base LLM</h3>
                <p>Run the same query through a raw Llama 3.3 baseline and the full agentic RAG pipeline, then compare quality side by side.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Comparison", key="btn_compare", use_container_width=True, type="primary"):
            st.session_state.mode = "compare"
            clear_run_state()
            st.rerun()

# ─────────────────────────────────────────────────────────
# Mode Execution Screen
# ─────────────────────────────────────────────────────────
else:
    mode_titles = {
        "knowledge_base": "Build Knowledge Base",
        "agentic_rag": "Agentic RAG Research",
        "compare": "RAG vs Base LLM Comparison"
    }
    mode_icons = {
        "knowledge_base": "📦",
        "agentic_rag": "🔬",
        "compare": "⚖️"
    }

    # Back button
    if st.button("← Back to Main Menu", key="btn_back"):
        reset_to_landing()
        st.rerun()

    st.markdown(
        f'<div class="breadcrumb">Research Assistant  ›  '
        f'<span class="breadcrumb-active">{mode_icons[st.session_state.mode]} {mode_titles[st.session_state.mode]}</span></div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Enter your research topic:",
        placeholder="e.g. 'Transformer architecture advances in 2025' or 'RAG pipeline deployment on AWS'",
        value=st.session_state.current_run["topic"] if st.session_state.current_run else ""
    )

    run_btn = st.button("▶  Run Research", type="primary")

    # Trigger execution
    if run_btn and topic:
        st.session_state.is_running = True
        st.session_state.current_run = {
            "topic": topic,
            "mode": st.session_state.mode,
            "progress": 0,
            "checklist": {
                "Intent Classification": "pending",
                "Retrieval": "pending",
                "Web Search": "pending",
                "Synthesis & Report": "pending",
                "Vector DB Upsert": "pending"
            },
            "metrics": {
                "sources": 0,
                "documents": 0,
                "chunks": 0,
                "embeddings": 0
            },
            "documents": [],
            "answer": "",
            "baseline_answer": ""
        }

    # ── Execution Display ──
    if st.session_state.is_running and st.session_state.current_run:
        run_data = st.session_state.current_run

        col_left, col_right = st.columns([2, 3])

        with col_left:
            st.markdown('<div class="section-label">Pipeline Progress</div>', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            checklist_placeholder = st.empty()
            metrics_placeholder = st.empty()

        with col_right:
            st.markdown('<div class="section-label">Live Document Feed</div>', unsafe_allow_html=True)
            docs_placeholder = st.empty()

        status_box = st.status("Agent is thinking…", expanded=True)

        # Start execution backend
        from agentic_research_rag.llm_client import reset_token_usage, get_token_usage
        import time

        agent = ResearchAgent()
        chunker = DocumentChunker()

        # 1. Compare Mode: Run Baseline LLM First
        if run_data["mode"] == "compare":
            status_box.update(label="Querying Baseline Llama 3.3…", state="running")
            baseline_agent = BaselineAgent()

            reset_token_usage()
            start_time = time.time()

            run_data["baseline_answer"] = baseline_agent.run(topic)

            latency = time.time() - start_time
            usage = get_token_usage()
            run_data["baseline_metrics"] = {
                "latency": latency,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }

        reset_token_usage()
        rag_start_time = time.time()

        # 2. Run LangGraph Stream
        try:
            for event in agent.stream_run(topic):
                for node_name, state_update in event.items():
                    if node_name == "classify":
                        run_data["checklist"]["Intent Classification"] = "completed"
                        if state_update.get("is_research"):
                            status_box.write("✅ **Intent:** Valid research topic.")
                            run_data["progress"] = 20
                        else:
                            status_box.write("❌ **Intent:** Not a research topic.")
                            run_data["answer"] = state_update.get("final_answer", "Invalid topic.")
                            run_data["progress"] = 100
                            break

                    elif node_name == "retrieve":
                        run_data["checklist"]["Retrieval"] = "completed"
                        chunks = state_update.get("retrieved_chunks", [])
                        status_box.write(f"📥 **Retrieval:** Fetched {len(chunks)} relevant chunks from vector store.")
                        run_data["progress"] = 40
                        
                        # Cache hit check
                        if state_update.get("final_answer"):
                            run_data["answer"] = state_update.get("final_answer")
                            run_data["checklist"]["Web Search"] = "cached"
                            run_data["checklist"]["Synthesis & Report"] = "completed"
                            run_data["checklist"]["Vector DB Upsert"] = "cached"
                            run_data["progress"] = 100
                            status_box.write("💡 **Cache Hit:** Found exact previous answer in database. Displaying cached report.")

                    elif node_name == "search":
                        run_data["checklist"]["Web Search"] = "completed"
                        docs = state_update.get("documents", [])

                        run_data["documents"] = [
                            {"title": doc.title, "url": doc.url}
                            for doc in docs
                        ]
                        run_data["metrics"]["documents"] = len(docs)
                        run_data["metrics"]["sources"] = sum(len(doc.metadata.get("citations", [])) for doc in docs)
                        status_box.write(f"🔍 **Search:** Retrieved {len(docs)} reports.")
                        run_data["progress"] = 60

                    elif node_name == "synthesize":
                        run_data["checklist"]["Synthesis & Report"] = "completed"
                        run_data["answer"] = state_update.get("final_answer", "")
                        run_data["progress"] = 80
                        status_box.write("✍️ **Synthesis:** Report compiled successfully.")

                    elif node_name == "process":
                        run_data["checklist"]["Vector DB Upsert"] = "completed"
                        status_box.write("⚙️ **Processing:** Chunked and upserted into vector store.")
                        run_data["progress"] = 100

                        if run_data["mode"] == "knowledge_base":
                            run_data["answer"] = f"Successfully compiled and uploaded knowledge base chunks for: **{topic}**."
                            break

                # Update live UI
                progress_bar.progress(run_data["progress"])
                checklist_placeholder.markdown(render_pipeline(run_data["checklist"], run_data["progress"]), unsafe_allow_html=True)

                if run_data["checklist"]["Vector DB Upsert"] == "completed":
                    run_data["metrics"]["chunks"] = run_data["metrics"]["documents"] * 12
                    run_data["metrics"]["embeddings"] = run_data["metrics"]["chunks"]

                metrics_placeholder.markdown(render_metrics(run_data["metrics"]), unsafe_allow_html=True)
                docs_placeholder.markdown(render_docs(run_data["documents"]), unsafe_allow_html=True)

                if run_data["progress"] == 100:
                    break

            rag_latency = time.time() - rag_start_time
            rag_usage = get_token_usage()
            run_data["rag_metrics"] = {
                "latency": rag_latency,
                "prompt_tokens": rag_usage.prompt_tokens,
                "completion_tokens": rag_usage.completion_tokens,
                "total_tokens": rag_usage.total_tokens,
            }

            status_box.update(label="Research Complete!", state="complete", expanded=False)

            st.session_state.history.append(run_data)
            st.session_state.current_run = run_data
            st.session_state.is_running = False
            st.rerun()

        except Exception as e:
            status_box.update(label="An error occurred during execution", state="error")
            st.error(f"Execution Error: {e}")
            st.session_state.is_running = False

    # ── Display Final Results ──
    elif st.session_state.current_run:
        run_data = st.session_state.current_run

        col_left, col_right = st.columns([2, 3])
        with col_left:
            st.markdown('<div class="section-label">Pipeline Status</div>', unsafe_allow_html=True)
            st.markdown(render_pipeline(run_data["checklist"], 100), unsafe_allow_html=True)
            st.markdown(render_metrics(run_data["metrics"]), unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="section-label">Referenced Documents</div>', unsafe_allow_html=True)
            st.markdown(render_docs(run_data["documents"]), unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── Comparison View ──
        if run_data["mode"] == "compare":
            col_b, col_a = st.columns(2)
            with col_b:
                st.markdown("""
                <div class="comparison-header">
                    <span class="comparison-badge badge-baseline">Baseline</span>
                    <span style="color: var(--text-primary); font-weight: 600;">Llama 3.3 — No RAG</span>
                </div>
                """, unsafe_allow_html=True)
                if "baseline_metrics" in run_data:
                    m = run_data["baseline_metrics"]
                    cost = (m["prompt_tokens"] * 0.59 / 1e6) + (m["completion_tokens"] * 0.79 / 1e6)
                    rate = m["completion_tokens"] / m["latency"] if m["latency"] > 0 else 0
                    st.markdown(
                        f'<div class="metrics-bar">'
                        f'<span>{m["latency"]:.1f}s</span> latency · '
                        f'<span>{m["total_tokens"]}</span> tokens · '
                        f'<span>${cost:.5f}</span> cost · '
                        f'<span>{rate:.0f}</span> tok/s'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(f'<div class="report-card">{run_data["baseline_answer"]}</div>', unsafe_allow_html=True)

            with col_a:
                st.markdown("""
                <div class="comparison-header">
                    <span class="comparison-badge badge-rag">Agentic RAG</span>
                    <span style="color: var(--text-primary); font-weight: 600;">Llama 3.3 + Web Search</span>
                </div>
                """, unsafe_allow_html=True)
                if "rag_metrics" in run_data:
                    m = run_data["rag_metrics"]
                    cost = (m["prompt_tokens"] * 0.59 / 1e6) + (m["completion_tokens"] * 0.79 / 1e6)
                    rate = m["completion_tokens"] / m["latency"] if m["latency"] > 0 else 0
                    st.markdown(
                        f'<div class="metrics-bar">'
                        f'<span>{m["latency"]:.1f}s</span> latency · '
                        f'<span>{m["total_tokens"]}</span> tokens · '
                        f'<span>${cost:.5f}</span> cost · '
                        f'<span>{rate:.0f}</span> tok/s'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                st.markdown(f'<div class="report-card">{run_data["answer"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="section-label">Generated Report</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="report-card">{run_data["answer"]}</div>', unsafe_allow_html=True)

            st.download_button(
                label="📥  Download Report",
                data=run_data["answer"],
                file_name=f"report_{topic.replace(' ', '_').lower()}.md",
                mime="text/markdown"
            )
