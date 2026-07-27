import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from agentic_research_rag.processing.embedding import GeminiEmbedder

# Sample texts with distinct subtopics
texts = [
    "Reinforcement learning algorithms for game playing",
    "Convolutional neural networks for image classification",
    "Natural language processing techniques for sentiment analysis",
    "Reinforcement learning in robotics",
    "Image segmentation using deep learning",
]

embedder = GeminiEmbedder()
chunks = []
for txt in texts:
    # Create a dummy Chunk object
    from agentic_research_rag.processing.models import Chunk
    chunk = Chunk(text=txt)
    chunks.append(chunk)

embedder.embed_chunks(chunks)
embeddings = np.array([c.embedding for c in chunks])

# Compute pairwise cosine similarity matrix
sim_matrix = cosine_similarity(embeddings)

print("Pairwise cosine similarity (rounded):")
for i, txt_i in enumerate(texts):
    row = " ".join([f"{sim_matrix[i, j]:.2f}" for j in range(len(texts))])
    print(f"{txt_i[:30]:30} -> {row}")
