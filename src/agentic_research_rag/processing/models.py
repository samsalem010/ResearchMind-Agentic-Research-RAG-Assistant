from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    Standard representation of a text chunk with its vector embedding.
    """

    text: str = Field(description="The text content of the chunk")
    embedding: list[float] | None = Field(
        default=None, description="The vector embedding of the text"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Metadata inherited from the source document (e.g., source url, citations)",
    )
