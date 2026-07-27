import time
from typing import Any

from langgraph.graph import END, START, StateGraph

from agentic_research_rag.agent.nodes import AgentNodes
from agentic_research_rag.agent.state import ResearchState
from agentic_research_rag.ingestion.search import WebSearcher
from agentic_research_rag.logger import logger
from agentic_research_rag.pipeline.retriever import Retriever
from agentic_research_rag.pipeline.synthesizer import Synthesizer
from agentic_research_rag.processing.chunking import DocumentChunker
from agentic_research_rag.processing.embedding import GeminiEmbedder
from agentic_research_rag.reporting.reporter import Reporter
from agentic_research_rag.storage.pinecone_db import PineconeDB


class ResearchAgent:
    """
    Orchestrates the iterative research workflow using LangGraph.
    """

    def __init__(self):
        logger.info("Initializing ResearchAgent dependencies...")
        self.searcher = WebSearcher()
        self.chunker = DocumentChunker()
        self.embedder = GeminiEmbedder()
        self.db = PineconeDB()
        self.retriever = Retriever(embedder=self.embedder, db=self.db)
        self.synthesizer = Synthesizer()
        self.llm_nodes = AgentNodes()
        self.reporter = Reporter()

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(ResearchState)

        # Add Nodes
        builder.add_node("classify", self.node_classify)
        builder.add_node("retrieve", self.node_retrieve)
        builder.add_node("reason", self.node_reason)
        builder.add_node("plan", self.node_plan)
        builder.add_node("search", self.node_search)
        builder.add_node("process", self.node_process)
        builder.add_node("synthesize", self.node_synthesize)

        # Add Edges
        builder.add_edge(START, "classify")

        # Conditional routing after classification
        builder.add_conditional_edges(
            "classify", self.route_after_classify, {"retrieve": "retrieve", "END": END}
        )

        builder.add_edge("retrieve", "reason")

        # Conditional routing after reasoning
        builder.add_conditional_edges(
            "reason", self.route_after_reason, {"plan": "plan", "synthesize": "synthesize"}
        )

        builder.add_edge("plan", "search")
        builder.add_edge("search", "process")
        builder.add_edge("process", "retrieve")  # loop back

        builder.add_edge("synthesize", END)

        return builder.compile()

    def node_classify(self, state: ResearchState) -> dict[str, Any]:
        topic = state["topic"]
        classification = self.llm_nodes.classify_intent(topic)
        is_res = classification.intent == "research_topic"

        ans = ""
        if not is_res:
            ans = f"I'm sorry, but '{topic}' doesn't seem to be a research topic. I am a specialized research assistant. Please rephrase your request as a topic to investigate."

        return {
            "is_research": is_res,
            "classification_reason": classification.reason,
            "final_answer": ans,
        }

    def route_after_classify(self, state: ResearchState) -> str:
        if state.get("is_research", False):
            return "retrieve"  # Check DB cache first
        return "END"

    def node_retrieve(self, state: ResearchState) -> dict[str, Any]:
        topic = state["topic"]
        namespace = topic[:20].replace(" ", "_").lower()

        chunks = self.retriever.retrieve(topic, namespace=namespace, top_k=10)

        # Check if there is an exact cached final answer
        cached_answer = ""
        for chunk in chunks:
            if not isinstance(chunk, str) and hasattr(chunk, "metadata") and chunk.metadata:
                if chunk.metadata.get("source") == "agent_synthesis" and chunk.metadata.get("topic") == topic:
                    cached_answer = chunk.text
                    break

        return {"retrieved_chunks": chunks, "final_answer": cached_answer}

    def node_reason(self, state: ResearchState) -> dict[str, Any]:
        # If we already found an exact cached answer, skip reasoning about context
        if state.get("final_answer"):
            return {"reasoning_gaps": ""}

        topic = state["topic"]
        chunks = state.get("retrieved_chunks", [])
        evaluation = self.llm_nodes.reason_about_context(topic, chunks)
        return {
            "reasoning_gaps": evaluation.gaps_description if evaluation.has_gaps else "",
        }

    def route_after_reason(self, state: ResearchState) -> str:
        gaps = state.get("reasoning_gaps", "")
        iteration = state.get("iteration", 0)

        if gaps and iteration < 3:
            return "plan"
        return "synthesize"

    def node_plan(self, state: ResearchState) -> dict[str, Any]:
        topic = state["topic"]
        gaps = state.get("reasoning_gaps", "")
        plan = self.llm_nodes.plan_queries(topic, gaps=gaps)
        return {
            "planned_queries": plan.queries,
            "iteration": state.get("iteration", 0) + 1,
        }

    def node_search(self, state: ResearchState) -> dict[str, Any]:
        queries = state.get("planned_queries", [])
        if not queries:
            queries = [state["topic"]]

        logger.info(f"Executing search for queries: {queries}")
        all_docs = []
        for q in queries:
            try:
                docs = self.searcher.search(q)
                all_docs.extend(docs)
            except Exception as e:
                logger.error(f"Search failed for query '{q}': {e}")

        existing_docs = state.get("documents", []) or []
        return {"documents": existing_docs + all_docs}

    def node_process(self, state: ResearchState) -> dict[str, Any]:
        topic = state["topic"]
        docs = state.get("documents", [])
        namespace = topic[:20].replace(" ", "_").lower()

        # Save downloaded documents to Pinecone (regular chunking)
        if docs:
            chunks = self.chunker.chunk_documents(docs)
            embedded_chunks = self.embedder.embed_chunks(chunks)
            self.db.upsert(embedded_chunks, namespace=namespace)

        return {"documents": []}

    def node_synthesize(self, state: ResearchState) -> dict[str, Any]:
        topic = state["topic"]
        final_answer = state.get("final_answer", "")
        if final_answer:
            logger.info("Using pre-existing final answer.")
            return {}

        retrieved_chunks = state.get("retrieved_chunks", [])
        documents = state.get("documents", [])

        # Format retrieved search documents into temporary chunks for the Synthesizer
        perplexity_chunks = []
        if documents:
            perplexity_chunks = self.chunker.chunk_documents(documents)

        # Combine both cached vector DB chunks and Perplexity search chunks
        all_chunks = retrieved_chunks + perplexity_chunks

        answer = self.synthesizer.synthesize(topic, all_chunks)
        report_path = self.reporter.generate_markdown_report(topic, answer)
        logger.info(f"Report saved to: {report_path}")

        return {"final_answer": answer}

    def run(self, topic: str) -> str:
        initial_state = {
            "topic": topic,
            "is_research": False,
            "classification_reason": "",
            "iteration": 0,
            "planned_queries": [],
            "documents": [],
            "retrieved_chunks": [],
            "reasoning_gaps": "",
            "final_answer": "",
        }

        final_state = self.graph.invoke(initial_state)
        return final_state.get("final_answer", "Failed to generate answer.")

    def stream_run(self, topic: str):
        """
        Yields intermediate graph states during execution.
        """
        initial_state = {
            "topic": topic,
            "is_research": False,
            "classification_reason": "",
            "iteration": 0,
            "planned_queries": [],
            "documents": [],
            "retrieved_chunks": [],
            "reasoning_gaps": "",
            "final_answer": "",
        }

        for output in self.graph.stream(initial_state):
            yield output
