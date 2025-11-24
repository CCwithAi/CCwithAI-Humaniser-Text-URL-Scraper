"""
Models for URL scraping and indexing
"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Literal


class ScrapeRequest(BaseModel):
    """Request to scrape and index a URL"""
    url: HttpUrl
    content_type: Literal["sales", "journalist"] = Field(
        description="Type of content: sales (marketing/commercial) or journalist (editorial/news)"
    )
    description: str = Field(
        min_length=5,
        max_length=200,
        description="Brief description of the content to help with indexing and retrieval"
    )


class ScrapeResponse(BaseModel):
    """Response from scraping operation"""
    success: bool
    message: str
    word_count: int = 0
    filename: str = ""
    error: str = ""
