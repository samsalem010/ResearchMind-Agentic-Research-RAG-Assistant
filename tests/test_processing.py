from unittest.mock import Mock, patch
import pytest

from agentic_research_rag.ingestion.models import Document
from agentic_research_rag.processing.chunking import DocumentChunker
from agentic_research_rag.processing.embedding import GeminiEmbedder
from agentic_research_rag.processing.models import Chunk


def test_document_chunker():
    doc = Document(
        url="https://example.com",
        title="Test Doc",
        content="This is a test document. " * 100,  # Long enough to trigger split
        metadata={"author": "AI"},
    )

    # Use very small chunks for testing
    chunker = DocumentChunker(chunk_size=50, chunk_overlap=10)
    chunks = chunker.chunk_documents([doc])

    assert len(chunks) > 1
    assert isinstance(chunks[0], Chunk)
    assert chunks[0].metadata["source_url"] == "https://example.com"
    assert chunks[0].metadata["author"] == "AI"
    assert len(chunks[0].text) <= 50


@patch("agentic_research_rag.processing.embedding.SentenceTransformer")
def test_gemini_embedder_success(mock_transformer_class):
    # Setup mock for SentenceTransformer instance
    mock_model = Mock()
    # all-MiniLM-L6-v2 outputs 384-dimensional vectors
    mock_model.encode.return_value = Mock(
        tolist=Mock(return_value=[[0.1] * 384, [0.2] * 384])
    )
    mock_transformer_class.return_value = mock_model

    embedder = GeminiEmbedder()

    # Create fake chunks
    chunks = [Chunk(text="Chunk 1", metadata={}), Chunk(text="Chunk 2", metadata={})]

    # Run embedder
    embedded_chunks = embedder.embed_chunks(chunks)

    assert len(embedded_chunks) == 2
    assert len(embedded_chunks[0].embedding) == 384
    assert len(embedded_chunks[1].embedding) == 384
    assert embedded_chunks[0].embedding == [0.1] * 384
    assert embedded_chunks[1].embedding == [0.2] * 384


@patch("agentic_research_rag.processing.embedding.SentenceTransformer")
def test_gemini_embedder_failure_fallback(mock_transformer_class):
    # Setup mock to throw an exception
    mock_model = Mock()
    mock_model.encode.side_effect = Exception("Inference failed")
    mock_transformer_class.return_value = mock_model

    embedder = GeminiEmbedder()
    chunks = [Chunk(text="Test chunk", metadata={})]
    embedded = embedder.embed_chunks(chunks)
    assert len(embedded) == 1
    assert embedded[0].embedding == [1e-5] * 384


@patch("agentic_research_rag.processing.embedding.SentenceTransformer")
def test_gemini_embedder_empty(mock_transformer_class):
    mock_model = Mock()
    mock_transformer_class.return_value = mock_model

    embedder = GeminiEmbedder()
    chunks = []
    assert embedder.embed_chunks(chunks) == []
    mock_model.encode.assert_not_called()
