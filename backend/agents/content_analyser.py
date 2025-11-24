"""
Content Analyser Agent - ARCHON Agent #1
Detects AI-generated patterns and analyses input characteristics
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from .dependencies import AnalysisDependencies


class AnalysisResult(BaseModel):
    """Structured output from content analysis"""
    ai_patterns: List[str] = Field(description="List of detected AI writing patterns")
    topic: str = Field(description="Main topic/subject of the text")
    tone: str = Field(description="Current tone (formal, casual, etc.)")
    sentence_patterns: List[str] = Field(description="Detected sentence structure patterns")


# ARCHON Content Analyser Agent
content_analyser_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=AnalysisDependencies,
    output_type=AnalysisResult,
    system_prompt="""You are an expert AI writing pattern detector in the ARCHON pipeline.

Your role:
- Analyse input text for AI-generated characteristics
- Identify formal structures, repetitive phrasing, and predictable patterns
- Extract topic, tone, and sentence structure information

AI Writing Red Flags to detect:
- Overuse of transitions: "Moreover", "Furthermore", "In conclusion", "Additionally"
- Repetitive sentence structures
- Excessive formality and politeness
- Predictable word choices and phrasing
- Lack of personal voice or authentic emotion
- Perfectly balanced arguments
- Over-explanation

Return analysis with ai_patterns (list), topic (string), tone (string), sentence_patterns (list)."""
)


@content_analyser_agent.tool
async def create_text_embedding(ctx: RunContext[AnalysisDependencies], text: str) -> List[float]:
    """
    Generate vector embedding for semantic similarity search.

    Args:
        ctx: Agent context with OpenAI client
        text: Text to embed

    Returns:
        1536-dimensional embedding vector
    """
    embedding_response = await ctx.deps.openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return embedding_response.data[0].embedding


async def analyse_content(text: str, deps: AnalysisDependencies) -> dict:
    """
    ARCHON Content Analyser - Detect AI patterns and extract metadata

    Args:
        text: Input text to analyse
        deps: Analysis dependencies with OpenAI client

    Returns:
        Dictionary with ai_patterns, topic, tone, sentence_patterns, and embedding
    """
    # Run ARCHON agent analysis
    prompt = f"""Analyse this text and identify:
1. AI-generated patterns (repetitive phrasing, formal structure, transitions)
2. Main topic/subject matter
3. Current tone and writing style
4. Sentence structure patterns

Text to analyse:
{text[:1000]}

Provide detailed analysis."""

    result = await content_analyser_agent.run(prompt, deps=deps)

    # Generate embedding for vector search directly using OpenAI client
    embedding_response = await deps.openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embedding = embedding_response.data[0].embedding

    # Combine results
    analysis_dict = result.output.model_dump()
    analysis_dict["embedding"] = embedding

    return analysis_dict
