from unittest.mock import patch

from agentic_research_rag.agent.nodes import IntentClassification, QueryPlan, ReasoningEvaluation


@patch("agentic_research_rag.agent.graph.WebSearcher")
@patch("agentic_research_rag.agent.graph.DocumentChunker")
@patch("agentic_research_rag.agent.graph.GeminiEmbedder")
@patch("agentic_research_rag.agent.graph.PineconeDB")
@patch("agentic_research_rag.agent.graph.Retriever")
@patch("agentic_research_rag.agent.graph.Synthesizer")
@patch("agentic_research_rag.agent.graph.AgentNodes")
def test_agent_graph_research_flow_no_cache(
    mock_nodes_class,
    mock_synth_class,
    mock_retriever_class,
    mock_pinecone_class,
    mock_embedder_class,
    mock_chunker_class,
    mock_searcher_class,
):
    # Simulate first pass finding gaps (cache miss), second pass finding no gaps
    mock_nodes = mock_nodes_class.return_value
    mock_nodes.classify_intent.return_value = IntentClassification(
        intent="research_topic", reason="Valid"
    )
    mock_nodes.plan_queries.return_value = QueryPlan(queries=["q1", "q2", "q3"])
    mock_nodes.reason_about_context.side_effect = [
        ReasoningEvaluation(has_gaps=True, gaps_description="Missing stuff"),
        ReasoningEvaluation(has_gaps=False, gaps_description=""),
    ]

    mock_searcher = mock_searcher_class.return_value
    mock_searcher.search.return_value = ["fake_doc"]

    mock_chunker = mock_chunker_class.return_value
    mock_chunker.chunk_documents.return_value = ["fake_chunk"]

    mock_embedder = mock_embedder_class.return_value
    mock_embedder.embed_chunks.return_value = ["embedded_chunk"]

    mock_pinecone = mock_pinecone_class.return_value

    mock_retriever = mock_retriever_class.return_value
    mock_retriever.retrieve.return_value = ["retrieved_chunk"]

    mock_synth = mock_synth_class.return_value
    mock_synth.synthesize.return_value = "The final answer is 42."

    from agentic_research_rag.agent.graph import ResearchAgent

    agent = ResearchAgent()

    # Run the graph
    answer = agent.run("What is the meaning of life?")

    assert answer == "The final answer is 42."
    mock_nodes.classify_intent.assert_called_once()
    mock_nodes.plan_queries.assert_called_once()
    assert mock_searcher.search.call_count == 3
    mock_chunker.chunk_documents.assert_called_once()
    mock_embedder.embed_chunks.assert_called_once()
    mock_pinecone.upsert.assert_called_once()
    assert mock_retriever.retrieve.call_count == 2  # Called once initially, once after search loop
    assert mock_nodes.reason_about_context.call_count == 2
    mock_synth.synthesize.assert_called_once()


@patch("agentic_research_rag.agent.graph.WebSearcher")
@patch("agentic_research_rag.agent.graph.DocumentChunker")
@patch("agentic_research_rag.agent.graph.GeminiEmbedder")
@patch("agentic_research_rag.agent.graph.PineconeDB")
@patch("agentic_research_rag.agent.graph.Retriever")
@patch("agentic_research_rag.agent.graph.Synthesizer")
@patch("agentic_research_rag.agent.graph.AgentNodes")
def test_agent_graph_semantic_cache_hit(
    mock_nodes_class,
    mock_synth_class,
    mock_retriever_class,
    mock_pinecone_class,
    mock_embedder_class,
    mock_chunker_class,
    mock_searcher_class,
):
    # Simulate DB already having the perfect answer (Cache Hit)
    mock_nodes = mock_nodes_class.return_value
    mock_nodes.classify_intent.return_value = IntentClassification(
        intent="research_topic", reason="Valid"
    )

    # Reason node says NO GAPS on the very first try
    mock_nodes.reason_about_context.return_value = ReasoningEvaluation(
        has_gaps=False, gaps_description=""
    )

    mock_searcher = mock_searcher_class.return_value
    mock_chunker = mock_chunker_class.return_value
    mock_embedder = mock_embedder_class.return_value
    mock_pinecone = mock_pinecone_class.return_value

    mock_retriever = mock_retriever_class.return_value
    mock_retriever.retrieve.return_value = ["excellent_retrieved_chunk_from_db"]

    mock_synth = mock_synth_class.return_value
    mock_synth.synthesize.return_value = "The cached final answer."

    from agentic_research_rag.agent.graph import ResearchAgent

    agent = ResearchAgent()

    # Run the graph
    answer = agent.run("Cached topic")

    assert answer == "The cached final answer."

    # Verify the short-circuit happened!
    mock_nodes.classify_intent.assert_called_once()
    mock_retriever.retrieve.assert_called_once()
    mock_nodes.reason_about_context.assert_called_once()
    mock_synth.synthesize.assert_called_once()

    # The crucial part: these should NEVER be called on a cache hit
    mock_nodes.plan_queries.assert_not_called()
    mock_searcher.search.assert_not_called()
    mock_chunker.chunk_documents.assert_not_called()
    mock_embedder.embed_chunks.assert_not_called()
    mock_pinecone.upsert.assert_not_called()


@patch("agentic_research_rag.agent.graph.AgentNodes")
def test_agent_graph_non_research(mock_nodes_class):
    mock_nodes = mock_nodes_class.return_value
    mock_nodes.classify_intent.return_value = IntentClassification(
        intent="not_research", reason="Command"
    )

    from agentic_research_rag.agent.graph import ResearchAgent

    # We patch all other dependencies to prevent errors if they are instantiated
    with (
        patch("agentic_research_rag.agent.graph.WebSearcher"),
        patch("agentic_research_rag.agent.graph.DocumentChunker"),
        patch("agentic_research_rag.agent.graph.GeminiEmbedder"),
        patch("agentic_research_rag.agent.graph.PineconeDB"),
        patch("agentic_research_rag.agent.graph.Retriever"),
        patch("agentic_research_rag.agent.graph.Synthesizer"),
    ):
        agent = ResearchAgent()
        answer = agent.run("Write me a poem.")

        assert "I'm sorry" in answer
        assert "doesn't seem to be a research topic" in answer
        mock_nodes.plan_queries.assert_not_called()
