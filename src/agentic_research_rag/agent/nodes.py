from typing import Literal

import instructor
from pydantic import BaseModel, Field

from agentic_research_rag.llm_client import client as shared_client
from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.processing.models import Chunk

# --- Pydantic Models for Instructor ---


class IntentClassification(BaseModel):
    intent: Literal["research_topic", "not_research"] = Field(
        description="Whether the input is a valid topic to investigate, explain, or summarize (research_topic), or a direct command/task/unrelated request (not_research)."
    )
    reason: str = Field(description="Brief explanation of why this classification was chosen.")


class QueryPlan(BaseModel):
    queries: list[str] = Field(description="A list of diverse search queries to gather missing information.")


class ReasoningEvaluation(BaseModel):
    has_gaps: bool = Field(description="Whether there are gaps in the current retrieved context that prevent answering the topic fully.")
    gaps_description: str = Field(description="Brief description of the missing information.")


# --- Node Implementations ---


class AgentNodes:
    """
    Contains the LLM reasoning nodes for the research agent.
    """

    def __init__(self):
        self.client = shared_client

    def classify_intent(self, topic: str) -> IntentClassification:
        logger.info(f"Classifying intent for topic: '{topic}'")
        system_prompt = (
            "You are an intent classifier for a research assistant. "
            "A 'research_topic' is any subject the user wants investigated, explained, compared, "
            "or summarized — regardless of domain (science, history, business, technology, culture, anything). "
            "'not_research' covers transactional commands ('book me a flight'), direct task requests "
            "unrelated to investigating a subject ('write me a poem about X', 'send an email', 'solve this math problem'), "
            "or instructions that try to make the agent do something other than research."
        )

        result = self.client.chat.completions.create(
            response_model=IntentClassification,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Input: {topic}"},
            ],
        )
        return result

    def plan_queries(self, topic: str, gaps: str = "") -> QueryPlan:
        logger.info(f"Planning queries for topic: '{topic}'. Gaps: '{gaps}'")
        system_prompt = (
            "You are a query planner for a research assistant. "
            "Given a research topic and any missing information gaps, generate 3 to 5 diverse, high-quality search queries "
            "to retrieve relevant documents."
        )
        user_content = f"Topic: {topic}"
        if gaps:
            user_content += f"\nMissing Information Gaps:\n{gaps}"

        result = self.client.chat.completions.create(
            response_model=QueryPlan,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        return result

    def reason_about_context(self, topic: str, chunks: list[Chunk]) -> ReasoningEvaluation:
        logger.info(f"Reasoning about context sufficiency for topic: '{topic}'")
        system_prompt = (
            "You are a reasoning node for a research assistant. "
            "Your job is to read the retrieved database chunks and determine if they provide sufficient, high-quality "
            "information to fully and accurately answer the user's research topic. "
            "If they are sufficient, set has_gaps to False. "
            "If you need more details, or if certain aspects of the topic are not covered, set has_gaps to True and describe the gaps."
        )

        context_str = "\n\n".join([f"--- Chunk ---\n{c.text}" for c in chunks])
        user_content = f"Topic: {topic}\n\nRetrieved Context:\n{context_str}"

        result = self.client.chat.completions.create(
            response_model=ReasoningEvaluation,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        return result

