from langsmith import traceable

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.llm_client import generate_text
from agentic_research_rag.reporting.reporter import Reporter


class BaselineAgent:
    """
    A simple, non-agentic baseline that answers queries directly using a single LLM call.
    No web search, no iterative reasoning.
    Uses Google's Gemini models via the OpenAI-compatible endpoint.
    """

    def __init__(self):
        pass
        self.reporter = Reporter()

    @traceable(name="Baseline_LLM_Call")
    def run(self, topic: str) -> str:
        """
        Generates an answer using a simple zero-shot prompt.
        """
        logger.info(f"Generating baseline answer for topic: '{topic}'")

        system_prompt = (
            "You are a helpful and knowledgeable assistant. "
            "Please provide a comprehensive answer to the user's topic based purely on your internal knowledge."
        )

        prompt = f"{system_prompt}\n\nTopic: {topic}"

        try:
            answer = generate_text(prompt)
            
            # Save the baseline report
            baseline_topic = f"baseline_{topic}"
            report_path = self.reporter.generate_markdown_report(baseline_topic, answer)
            logger.info(f"Baseline report saved to: {report_path}")
            
            return answer
        except Exception as e:
            logger.error(f"Baseline LLM call failed: {e}")
            return "Failed to generate baseline answer."
