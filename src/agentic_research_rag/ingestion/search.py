import requests
from langsmith import traceable

from agentic_research_rag.config import settings
from agentic_research_rag.ingestion.models import Document
from agentic_research_rag.logger import logger


class WebSearcher:
    """
    Handles web search operations using Perplexity API's online models.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.perplexity_api_key

        if not self.api_key:
            raise ValueError("Perplexity API key is missing. Set PERPLEXITY_API_KEY in environment.")

    @traceable(name="Perplexity_Search")
    def search(self, query: str, max_results: int = 5) -> list[Document]:
        """
        Executes a web search via Perplexity and returns a synthesized Document with citations.
        Note: max_results is ignored since Perplexity provides a single unified answer.
        """
        logger.info(f"Executing Perplexity web search for query: '{query}'")

        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a research assistant. Search across many sources, evaluate them, and synthesize a comprehensive, detailed answer citing all relevant sources."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.1
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"Perplexity Search failed: {e}")
            raise

        # Log the raw Perplexity response structure and metadata
        citations = data.get("citations", [])
        logger.info(f"Raw Perplexity response metadata for query '{query}': choices={len(data.get('choices', []))}, citations_count={len(citations)}, citations={citations}")

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        # We return a single rich document representing the synthesized report,
        # but preserving all citation URLs in the metadata list so they can be counted as sources.
        doc = Document(
            url=citations[0] if citations else "",
            title=f"Perplexity Report: {query}",
            content=content,
            metadata={"source": "perplexity", "citations": citations},
        )

        logger.info(f"Retrieved synthesized report from Perplexity with {len(citations)} citations.")
        return [doc]
