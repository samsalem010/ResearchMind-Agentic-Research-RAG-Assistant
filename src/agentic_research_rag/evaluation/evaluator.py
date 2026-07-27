from agentic_research_rag.llm_client import client as shared_client

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.evaluation.models import ComparisonResult


class Evaluator:
    """
    Uses an advanced LLM (gpt-4o) via Instructor to judge two answers side-by-side.
    """

    def __init__(self):
        self.client = shared_client

    def evaluate_answers(
        self, topic: str, baseline_answer: str, agent_answer: str
    ) -> ComparisonResult:
        """
        Evaluates the baseline answer vs the agent answer and returns a structured ComparisonResult.
        """
        logger.info(f"Evaluating answers for topic: '{topic}'")

        system_prompt = (
            "You are an impartial, expert judge evaluating two research reports on a given topic. "
            "You will be provided with the Topic, Answer 1 (Baseline), and Answer 2 (Agentic RAG). "
            "Please score both answers on a scale of 1-5 for Comprehensiveness, Recency, Factual Accuracy, and Citations. "
            "Finally, declare a winner ('baseline', 'agent', or 'tie') and provide a brief justification."
        )

        user_prompt = f"""Topic: {topic}

=== Answer 1 (Baseline) ===
{baseline_answer}

=== Answer 2 (Agent) ===
{agent_answer}
"""

        result = self.client.chat.completions.create(
            response_model=ComparisonResult,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return result
