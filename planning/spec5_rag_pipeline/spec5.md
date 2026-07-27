# Spec 5: RAG Pipeline

## Goal
Build the core Retrieval-Augmented Generation (RAG) logic that connects our storage to a generative AI model.

## Scope
- Create a `Retriever` class that takes a user query, embeds it using `OpenAIEmbedder`, and fetches relevant `Chunk` objects from `PineconeDB`. Supports namespace scoping.
- Create a `Synthesizer` class that formats a prompt with retrieved chunks and calls OpenAI's chat completions to generate a cited final answer.
- Create unit tests mocking OpenAI and Pinecone for the pipeline.
- *Note: These modules are now orchestrated by LangGraph as the `retrieve` and `synthesize` nodes in Spec 6.*
