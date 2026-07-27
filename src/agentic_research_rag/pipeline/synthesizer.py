from langsmith import traceable

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.llm_client import generate_text
from agentic_research_rag.processing.models import Chunk


class Synthesizer:
    """
    Generates final answers using an LLM, augmented by retrieved chunks.
    Uses Google's Gemini models via the OpenAI-compatible endpoint.
    """

    def __init__(self):
        pass

    def synthesize(self, query: str, context_chunks: list[Chunk]) -> str:
        """
        Generates an answer to the query using the provided context chunks.
        """
        logger.info(f"Synthesizing answer for query: '{query}' using {len(context_chunks)} chunks.")

        if not context_chunks:
            return "I could not find any relevant information to answer your question."

        # Format the context
        context_text = "\n\n".join(
            [
                f"--- Context {i + 1} ---\n{c.text}\nSource: {c.metadata.get('source', 'Unknown')}"
                for i, c in enumerate(context_chunks)
            ]
        )

        system_prompt = (
            "You are an expert AI research assistant. Your task is to evaluate all the provided context and synthesize a comprehensive, detailed, and structured research report addressing the user's topic.\n\n"
            "Guidelines:\n"
            "1. Synthesize information from all the relevant sources in the context to form a complete, objective, and detailed answer.\n"
            "2. The length of the answer should be proportional to the complexity of the topic: write a comprehensive report of maximum 6 to 10 paragraphs, but it can be as short as 1 to 2 lines if the question is extremely direct or simple.\n"
            "3. Structure your response logically using markdown headers, lists, and bold text where appropriate to make it highly readable.\n"
            "4. Include inline citations or refer to the sources where appropriate (e.g., [Title of Source](URL)).\n"
            "5. Do not invent or extrapolate facts; rely strictly on the provided context."
        )

        prompt = f"System Instructions:\n{system_prompt}\n\nContext Information:\n{context_text}\n\nQuestion/Topic to Research: {query}"

        logger.info(f"Generating final synthesis report.")
        
        try:
            return generate_text(prompt)
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            raise
