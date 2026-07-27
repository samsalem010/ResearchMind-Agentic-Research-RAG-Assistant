from unittest.mock import Mock, patch
from agentic_research_rag.processing.models import Chunk

from agentic_research_rag.pipeline.retriever import Retriever
from agentic_research_rag.pipeline.synthesizer import Synthesizer
from agentic_research_rag.processing.models import Chunk


def test_retriever():
    mock_embedder = Mock()
    mock_db = Mock()

    # Mock embedder returning a chunk with an embedding
    mock_embedded_chunk = Chunk(text="test query", embedding=[0.1, 0.2])
    mock_embedder.embed_chunks.return_value = [mock_embedded_chunk]

    # Mock DB returning a list of chunks
    mock_result_chunk = Chunk(text="Found info", metadata={"source": "url"})
    mock_db.search.return_value = [mock_result_chunk]

    retriever = Retriever(embedder=mock_embedder, db=mock_db)
    results = retriever.retrieve("test query")

    assert len(results) == 1
    assert results[0].text == "Found info"
    mock_embedder.embed_chunks.assert_called_once()
    mock_db.search.assert_called_once_with(query_embedding=[0.1, 0.2], top_k=5, namespace="")


@patch("agentic_research_rag.pipeline.synthesizer.generate_text")
def test_synthesizer(mock_generate_text):
    mock_generate_text.return_value = "Here is the answer based on context."

    synthesizer = Synthesizer()

    chunks = [
        Chunk(text="Context 1", metadata={"source": "url1"}),
        Chunk(text="Context 2", metadata={"source": "url2"}),
    ]

    answer = synthesizer.synthesize("What is the meaning of life?", chunks)

    assert answer == "Here is the answer based on context."
    mock_generate_text.assert_called_once()

    # Verify prompt formatting
    call_args = mock_generate_text.call_args.args
    prompt = call_args[0]
    assert "Context 1" in prompt
    assert "url1" in prompt


def test_synthesizer_empty_context():
    synthesizer = Synthesizer()

    answer = synthesizer.synthesize("Hello?", [])
    assert "I could not find any relevant information" in answer
