from langchain_text_splitters import RecursiveCharacterTextSplitter

from agentic_research_rag.ingestion.models import Document
from agentic_research_rag.logger import logger
from agentic_research_rag.processing.models import Chunk


class DocumentChunker:
    """
    Splits Documents into semantic Chunks.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        """
        Takes a list of Documents and returns a flat list of Chunks.
        """
        logger.info(f"Chunking {len(documents)} documents...")
        all_chunks = []

        for doc in documents:
            if not doc.content.strip():
                continue

            texts = self.splitter.split_text(doc.content)

            # Inherit metadata from the parent document
            doc_metadata = doc.metadata.copy()
            doc_metadata["source_url"] = doc.url
            doc_metadata["source_title"] = doc.title

            for text in texts:
                chunk = Chunk(text=text, metadata=doc_metadata)
                all_chunks.append(chunk)

        logger.info(f"Created {len(all_chunks)} chunks.")
        return all_chunks
