from pydantic import BaseModel, Field
from typing import Literal, Optional


class HumaniseRequest(BaseModel):
    """Request model for text humanisation"""
    input_text: str = Field(..., min_length=10, max_length=10000)
    mode: Literal["sales", "journalist"] = Field(
        default="journalist",
        description="Transformation mode: sales or journalist"
    )


class HumaniseResponse(BaseModel):
    """Response model for humanised text"""
    output_text: str
    quality_score: float = Field(..., ge=0.0, le=1.0)
    iterations: int
    mode: str
    processing_time_ms: int
    metrics: Optional[dict] = None
