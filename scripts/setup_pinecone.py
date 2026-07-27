import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

from agentic_research_rag.config import settings
from agentic_research_rag.logger import logger

load_dotenv()


def setup_database():
    """
    Connects to Pinecone and provisions the vector database index if it does not already exist.
    """
    logger.info("Connecting to Pinecone...")
    
    if not settings.pinecone_api_key:
        logger.error("PINECONE_API_KEY is missing from the environment. Please add it to your .env file.")
        return

    pc = Pinecone(api_key=settings.pinecone_api_key)
    index_name = settings.pinecone_index_name or "agentic-research-index"

    existing_indexes = pc.list_indexes().names()
    
    if index_name in existing_indexes:
        logger.info(f"Deleting existing index '{index_name}' to recreate with 768 dimensions...")
        pc.delete_index(index_name)
    
    logger.info(f"Creating Pinecone index '{index_name}' with dimension 384 (all-MiniLM-L6-v2)...")
    pc.create_index(
        name=index_name,
        dimension=384,  # Standard for sentence-transformers/all-MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    logger.info(f"Successfully created index '{index_name}'.")

if __name__ == "__main__":
    setup_database()
