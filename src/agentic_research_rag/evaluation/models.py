from typing import Literal

from pydantic import BaseModel, Field


class EvaluationScore(BaseModel):
    comprehensiveness: int = Field(
        ge=1, le=5, description="Score from 1 to 5 on how comprehensively the topic was covered."
    )
    recency: int = Field(
        ge=1, le=5, description="Score from 1 to 5 on how recent and up-to-date the information is."
    )
    accuracy: int = Field(
        ge=1, le=5, description="Score from 1 to 5 on the factual accuracy and depth."
    )
    citations: int = Field(
        ge=1, le=5, description="Score from 1 to 5 on the presence and quality of source citations."
    )
    reasoning: str = Field(description="Explanation of why these scores were given.")


class ComparisonResult(BaseModel):
    baseline_score: EvaluationScore = Field(description="The evaluation score for the Baseline LLM.")
    agent_score: EvaluationScore = Field(description="The evaluation score for the Agentic RAG.")
    winner: Literal["baseline", "agent", "tie"] = Field(
        description="The decisive winner based on the criteria."
    )
    final_justification: str = Field(description="A brief justification for the declared winner.")
