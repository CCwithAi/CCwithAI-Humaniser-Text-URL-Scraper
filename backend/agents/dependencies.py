"""
ARCHON Agent Dependencies
Shared state and configuration for all agents in the pipeline
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from supabase import Client
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


@dataclass
class AgentDependencies:
    """Base dependencies for all ARCHON agents"""
    openai_client: AsyncOpenAI
    anthropic_client: AsyncAnthropic
    supabase_client: Optional[Client]


@dataclass
class AnalysisDependencies(AgentDependencies):
    """Dependencies for Content Analyser Agent"""
    pass


@dataclass
class RetrievalDependencies(AgentDependencies):
    """Dependencies for Content Retrieval Agent"""
    supabase_enabled: bool = False


@dataclass
class TransformationDependencies(AgentDependencies):
    """Dependencies for Style Transformer Agent"""
    human_examples: List[Dict] = None
    analysis_data: Dict = None

    def __post_init__(self):
        if self.human_examples is None:
            self.human_examples = []
        if self.analysis_data is None:
            self.analysis_data = {}


@dataclass
class QualityDependencies(AgentDependencies):
    """Dependencies for Quality Checker Agent"""
    original_text: str = ""
    mode: str = "journalist"


@dataclass
class OrchestrationDependencies:
    """Dependencies for ARCHON Orchestrator"""
    openai_api_key: str
    anthropic_api_key: str
    supabase_url: Optional[str]
    supabase_key: Optional[str]
    max_iterations: int = 3
    quality_threshold: float = 0.75

    def __post_init__(self):
        """Initialize clients"""
        self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
        self.anthropic_client = AsyncAnthropic(api_key=self.anthropic_api_key)

        # Initialize Supabase if credentials provided
        if self.supabase_url and self.supabase_key:
            from supabase import create_client
            self.supabase_client = create_client(self.supabase_url, self.supabase_key)
            self.supabase_enabled = True
        else:
            self.supabase_client = None
            self.supabase_enabled = False


def create_orchestration_deps() -> OrchestrationDependencies:
    """Factory function to create orchestration dependencies from environment"""
    return OrchestrationDependencies(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_KEY"),
        max_iterations=3,
        quality_threshold=0.75
    )
