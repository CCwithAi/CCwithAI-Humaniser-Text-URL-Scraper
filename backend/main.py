from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path

from agents.orchestrator import HumaniserOrchestrator
from models.request import HumaniseRequest, HumaniseResponse
from models.scraper import ScrapeRequest, ScrapeResponse
from services.url_scraper import URLScraperService
from agents.dependencies import create_orchestration_deps

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(
    title="AI Humaniser API",
    description="Transform AI-generated text into authentic human writing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = HumaniserOrchestrator()

# Initialize scraper service
deps = create_orchestration_deps()
scraper_service = URLScraperService(
    openai_client=deps.openai_client,
    supabase_client=deps.supabase_client
)


@app.get("/")
async def root():
    return {
        "message": "AI Humaniser API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/humanise", response_model=HumaniseResponse)
async def humanise_text(request: HumaniseRequest):
    """
    Transform AI-generated text into human-written style.

    Modes:
    - sales: Marketing/persuasive copy
    - journalist: Editorial/news content
    """
    try:
        result = await orchestrator.process(
            input_text=request.input_text,
            mode=request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/modes")
async def get_available_modes():
    """Get available transformation modes"""
    return {
        "modes": [
            {
                "id": "sales",
                "name": "Sales & Marketing",
                "description": "Conversational, persuasive copy with strong CTAs"
            },
            {
                "id": "journalist",
                "name": "Journalist & Editorial",
                "description": "Objective reporting with engaging narrative"
            }
        ]
    }


@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_and_index_url(request: ScrapeRequest):
    """
    Scrape content from a URL and index it to the training database.

    This endpoint:
    1. Scrapes the content from the provided URL using browser automation
    2. Extracts the main article/content text
    3. Generates embeddings for semantic search
    4. Saves the content to a file
    5. Indexes it to Supabase for use in humanization

    Args:
        request: ScrapeRequest with url, content_type, and description

    Returns:
        ScrapeResponse with success status and metadata
    """
    try:
        result = await scraper_service.scrape_and_index(
            url=str(request.url),
            content_type=request.content_type,
            description=request.description
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        return ScrapeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
