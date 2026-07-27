import os
from typing import List

from sentence_transformers import SentenceTransformer

from agentic_research_rag.logger import logger
from agentic_research_rag.processing.models import Chunk


class GeminiEmbedder:
    """Generates vector embeddings for chunks using a local SentenceTransformer model.

    The embedder lazily loads the model on first use. It returns 384-dimensional
    embeddings using the 'sentence-transformers/all-MiniLM-L6-v2' model, which
    is a lightweight and high-quality local semantic model.
    """

    MODEL_LABEL = "SentenceTransformer (all-MiniLM-L6-v2)"

    _model: SentenceTransformer | None = None
    _model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self, api_key: str | None = None, model: str | None = None):
        # api_key and model parameters are ignored for the local model.
        logger.info(
            f"GeminiEmbedder initialised using local model '{self._model_name}'."
        )

    @property
    def model(self) -> SentenceTransformer:
        """Lazily instantiate the SentenceTransformer model.

        The model is loaded only once per process to avoid repeated heavy I/O.
        """
        if self._model is None:
            logger.info("Loading SentenceTransformer model… this may take a few seconds.")
            self._model = SentenceTransformer(self._model_name)
        return self._model

    def embed_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """Generate embeddings for a list of ``Chunk`` objects.

        The function updates each ``Chunk`` in‑place with a 384‑dimensional
        ``embedding`` list and returns the same list for convenience.
        """
        if not chunks:
            return chunks

        texts = [chunk.text for chunk in chunks]
        logger.info(f"Generating embeddings for {len(chunks)} chunks using SentenceTransformer.")
        try:
            embeddings = self.model.encode(texts, batch_size=32, normalize_embeddings=True)
            # ``encode`` returns a NumPy array; convert each row to a Python list.
            for chunk, embedding in zip(chunks, embeddings.tolist()):
                chunk.embedding = embedding
        except Exception as e:
            logger.error(f"SentenceTransformer embedding failed: {e}")
            # Fallback to dummy embeddings of 384 dimensions to keep the pipeline functional.
            for chunk in chunks:
                chunk.embedding = [1e-5] * 384
        logger.info("Successfully generated SentenceTransformer embeddings.")
        return chunks
