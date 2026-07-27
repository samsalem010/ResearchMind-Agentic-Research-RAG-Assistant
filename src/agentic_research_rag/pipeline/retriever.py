from agentic_research_rag.logger import logger
from agentic_research_rag.processing.embedding import GeminiEmbedder
from agentic_research_rag.processing.models import Chunk
from agentic_research_rag.storage.pinecone_db import PineconeDB


class Retriever:
    """
    Retrieves relevant chunks from the Vector DB based on a text query.
    """

    def __init__(self, embedder: GeminiEmbedder, db: PineconeDB):
        self.embedder = embedder
        self.db = db

    def retrieve(self, query: str, top_k: int = 5, namespace: str = "") -> list[Chunk]:
        """
        Embeds the query and searches the database for relevant chunks.
        """
        logger.info(f"Retrieving top {top_k} chunks for query: '{query}'")

        # 1. Embed the query text
        # OpenAIEmbedder.embed_chunks takes a list of Chunks, so we wrap the query
        dummy_chunk = Chunk(text=query)
        embedded_chunks = self.embedder.embed_chunks([dummy_chunk])

        if not embedded_chunks or not embedded_chunks[0].embedding:
            logger.error("Failed to generate embedding for query.")
            return []

        query_vector = embedded_chunks[0].embedding

        # 2. Search the database
        results = self.db.search(query_embedding=query_vector, top_k=top_k, namespace=namespace)

        return results
