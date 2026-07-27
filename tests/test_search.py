from unittest.mock import Mock, patch

import pytest

from agentic_research_rag.ingestion.models import Document
from agentic_research_rag.ingestion.search import WebSearcher


@pytest.fixture
def mock_perplexity_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a detailed answer synthesized by Perplexity."
                }
            }
        ],
        "citations": [
            "https://example.com/source1",
            "https://example.com/source2"
        ]
    }


@patch("agentic_research_rag.ingestion.search.requests.post")
def test_web_searcher(mock_post, mock_perplexity_response):
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = mock_perplexity_response
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    # Initialize searcher
    searcher = WebSearcher(api_key="fake-key")
    docs = searcher.search("test query")

    # Assertions
    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert docs[0].title == "Perplexity Report: test query"
    assert docs[0].url == "https://example.com/source1"
    assert docs[0].content == "This is a detailed answer synthesized by Perplexity."
    assert docs[0].metadata["source"] == "perplexity"
    assert docs[0].metadata["citations"] == ["https://example.com/source1", "https://example.com/source2"]


def test_web_searcher_missing_keys():
    # Attempting to init without keys should raise ValueError
    with patch("agentic_research_rag.ingestion.search.settings") as mock_settings:
        mock_settings.perplexity_api_key = None
        with pytest.raises(ValueError, match="Perplexity API key is missing"):
            WebSearcher()
