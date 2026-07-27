import uuid

from pinecone import Pinecone
from langsmith import traceable

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger
from agentic_research_rag.processing.models import Chunk


class PineconeDB:
    """
    Handles interactions with the Pinecone Vector Database.
    """

    def __init__(self, api_key: str | None = None, index_name: str | None = None):
        self.api_key = api_key or settings.pinecone_api_key
        self.index_name = index_name or settings.pinecone_index_name

        if not self.api_key:
            raise ValueError("Pinecone API key is missing. Set PINECONE_API_KEY in environment.")

        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(self.index_name)

    @traceable(name="Pinecone_Upsert")
    def upsert(self, chunks: list[Chunk], namespace: str = "") -> None:
        """
        Uploads a list of Chunks to the Pinecone index.
        Note: Pinecone requires IDs, Vectors, and Metadata.
        """
        if not chunks:
            return

        logger.info(
            f"Upserting {len(chunks)} chunks to Pinecone index '{self.index_name}' "
            f"(namespace: '{namespace}')..."
        )

        vectors = []
        for chunk in chunks:
            if not chunk.embedding:
                logger.warning("Skipping chunk with no embedding.")
                continue

            # Generate a unique ID for the chunk if one isn't in metadata
            chunk_id = str(uuid.uuid4())

            # Pinecone metadata must be a flat dictionary of strings, numbers, booleans,
            # or lists of strings.
            # We must store the chunk text itself in the metadata so we can retrieve it!
            metadata = chunk.metadata.copy()
            metadata["text"] = chunk.text

            vectors.append(
                {
                    "id": chunk_id,
                    "values": chunk.embedding,
                    "metadata": metadata,
                }
            )

        try:
            # Upsert in batches of 100 to avoid payload limits
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i : i + batch_size]
                self.index.upsert(vectors=batch, namespace=namespace)
        except Exception as e:
            logger.error(f"Pinecone upsert failed: {e}")
            raise

        logger.info("Successfully upserted chunks to Pinecone.")

    @traceable(name="Pinecone_Retrieve")
    def search(
        self, query_embedding: list[float], top_k: int = 5, namespace: str = ""
    ) -> list[Chunk]:
        """
        Searches Pinecone for the top_k most similar chunks.
        """
        logger.info(
            f"Searching Pinecone index '{self.index_name}' for top {top_k} results "
            f"(namespace: '{namespace}')..."
        )

        try:
            response = self.index.query(
                namespace=namespace,
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
            )
        except Exception as e:
            logger.error(f"Pinecone search failed: {e}")
            raise

        results = []
        for match in response.get("matches", []):
            metadata = match.get("metadata", {})
            text = metadata.pop("text", "")  # Extract text, leave rest as metadata

            chunk = Chunk(
                text=text,
                embedding=match.get("values", []),
                metadata=metadata,
            )
            # Optionally add the similarity score to metadata
            chunk.metadata["score"] = match.get("score")
            results.append(chunk)

        logger.info(f"Retrieved {len(results)} matches from Pinecone.")
        return results
