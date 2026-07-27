from typing import TypedDict

from agentic_research_rag.ingestion.models import Document
from agentic_research_rag.processing.models import Chunk


class ResearchState(TypedDict):
    """
    Represents the state of our research agent as it moves through the LangGraph nodes.
    """

    topic: str
    is_research: bool
    classification_reason: str
    iteration: int
    planned_queries: list[str]
    documents: list[Document]
    retrieved_chunks: list[Chunk]
    reasoning_gaps: str
    final_answer: str
