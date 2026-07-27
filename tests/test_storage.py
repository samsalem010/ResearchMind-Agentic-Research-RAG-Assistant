from unittest.mock import Mock, patch

import pytest

from agentic_research_rag.processing.models import Chunk
from agentic_research_rag.storage.pinecone_db import PineconeDB


@patch("agentic_research_rag.storage.pinecone_db.Pinecone")
def test_pinecone_upsert(mock_pinecone_class):
    # Setup mock
    mock_pc_instance = Mock()
    mock_index = Mock()
    mock_pc_instance.Index.return_value = mock_index
    mock_pinecone_class.return_value = mock_pc_instance

    db = PineconeDB(api_key="fake-key", index_name="test-index")

    chunks = [
        Chunk(text="Chunk 1", embedding=[0.1, 0.2], metadata={"source": "test1"}),
        Chunk(text="Chunk 2", embedding=[0.3, 0.4], metadata={"source": "test2"}),
    ]

    db.upsert(chunks, namespace="test-ns")

    # Verify upsert was called with correct data
    mock_index.upsert.assert_called_once()

    # Extract the vectors argument from the call
    call_args, call_kwargs = mock_index.upsert.call_args
    vectors = call_kwargs.get("vectors")
    namespace = call_kwargs.get("namespace")

    assert namespace == "test-ns"
    assert len(vectors) == 2
    assert vectors[0]["values"] == [0.1, 0.2]
    assert vectors[0]["metadata"]["source"] == "test1"
    assert vectors[0]["metadata"]["text"] == "Chunk 1"


@patch("agentic_research_rag.storage.pinecone_db.Pinecone")
def test_pinecone_search(mock_pinecone_class):
    # Setup mock
    mock_pc_instance = Mock()
    mock_index = Mock()

    # Fake response
    mock_index.query.return_value = {
        "matches": [
            {
                "id": "123",
                "score": 0.95,
                "values": [],
                "metadata": {"text": "Found Chunk 1", "source": "test1"},
            }
        ]
    }

    mock_pc_instance.Index.return_value = mock_index
    mock_pinecone_class.return_value = mock_pc_instance

    db = PineconeDB(api_key="fake-key", index_name="test-index")

    results = db.search([0.1, 0.2], top_k=1)

    assert len(results) == 1
    assert isinstance(results[0], Chunk)
    assert results[0].text == "Found Chunk 1"
    assert results[0].metadata["source"] == "test1"
    assert results[0].metadata["score"] == 0.95


def test_pinecone_missing_keys():
    with patch("agentic_research_rag.storage.pinecone_db.settings") as mock_settings:
        mock_settings.pinecone_api_key = None
        with pytest.raises(ValueError, match="Pinecone API key is missing"):
            PineconeDB()
