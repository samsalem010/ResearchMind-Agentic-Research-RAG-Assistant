from pydantic import BaseModel, Field


class Document(BaseModel):
    """
    Standard representation of a document retrieved from any source.
    """

    url: str = Field(description="The source URL of the document")
    title: str = Field(default="", description="The title of the document")
    content: str = Field(description="The main text content of the document")
    metadata: dict = Field(
        default_factory=dict, description="Additional metadata (e.g., score, author)"
    )
