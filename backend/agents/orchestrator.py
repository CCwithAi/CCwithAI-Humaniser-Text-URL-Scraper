"""
ARCHON Multi-Agent Orchestrator
Coordinates all agents in the humanisation pipeline using Pydantic AI
"""
import time
from typing import Dict
from models.request import HumaniseResponse

from .dependencies import (
    create_orchestration_deps,
    AnalysisDependencies,
    RetrievalDependencies,
    TransformationDependencies,
    QualityDependencies
)
from .content_analyser import analyse_content
from .content_retrieval import retrieve_human_content
from .style_transformer import transform_to_human_style
from .quality_checker import evaluate_quality


class HumaniserOrchestrator:
    """
    ARCHON-based orchestrator managing the multi-agent pipeline
    for transforming AI text into human writing using Pydantic AI
    """

    def __init__(self):
        # Create orchestration dependencies
        self.deps = create_orchestration_deps()

        self.max_iterations = self.deps.max_iterations
        self.quality_threshold = self.deps.quality_threshold

    async def process(self, input_text: str, mode: str) -> HumaniseResponse:
        """
        Main ARCHON processing pipeline

        Flow:
        1. Content Analyser: Detect AI patterns
        2. Content Retrieval: Find similar human writing
        3. Style Transformer: Transform to human style
        4. Quality Checker: Validate output
        5. Iteration Controller: Refine if needed

        Args:
            input_text: AI-generated text to humanise
            mode: 'sales' or 'journalist'

        Returns:
            HumaniseResponse with transformed text and metrics
        """
        start_time = time.time()

        # Step 1: Analyse input content using ARCHON Content Analyser Agent
        analysis_deps = AnalysisDependencies(
            openai_client=self.deps.openai_client,
            anthropic_client=self.deps.anthropic_client,
            supabase_client=self.deps.supabase_client
        )

        analysis = await analyse_content(input_text, analysis_deps)

        # Step 2: Retrieve relevant human content using ARCHON Content Retrieval Agent
        retrieval_deps = RetrievalDependencies(
            openai_client=self.deps.openai_client,
            anthropic_client=self.deps.anthropic_client,
            supabase_client=self.deps.supabase_client,
            supabase_enabled=self.deps.supabase_enabled
        )

        human_examples = await retrieve_human_content(
            content_type=mode,
            topic=analysis.get("topic", "general"),
            embedding=analysis.get("embedding"),
            deps=retrieval_deps,
            limit=5
        )

        # Step 3-5: Transform with quality-driven iteration using ARCHON agents
        current_text = input_text
        iterations = 0
        quality_score = 0.0
        quality_result = {}

        for iteration in range(self.max_iterations):
            iterations += 1

            # Transform text using ARCHON Style Transformer Agent
            transformation_deps = TransformationDependencies(
                openai_client=self.deps.openai_client,
                anthropic_client=self.deps.anthropic_client,
                supabase_client=self.deps.supabase_client,
                human_examples=human_examples,
                analysis_data=analysis
            )

            transformed = await transform_to_human_style(
                text=current_text,
                mode=mode,
                human_examples=human_examples,
                analysis=analysis,
                deps=transformation_deps
            )

            # Check quality using ARCHON Quality Checker Agent
            quality_deps = QualityDependencies(
                openai_client=self.deps.openai_client,
                anthropic_client=self.deps.anthropic_client,
                supabase_client=self.deps.supabase_client,
                original_text=input_text,
                mode=mode
            )

            quality_result = await evaluate_quality(
                original=input_text,
                transformed=transformed,
                mode=mode,
                deps=quality_deps
            )

            quality_score = quality_result["score"]

            # Break if quality threshold met
            if quality_score >= self.quality_threshold:
                current_text = transformed
                break

            # Prepare for next iteration with feedback
            current_text = transformed
            analysis["feedback"] = quality_result.get("feedback", [])

        processing_time = int((time.time() - start_time) * 1000)

        return HumaniseResponse(
            output_text=current_text,
            quality_score=quality_score,
            iterations=iterations,
            mode=mode,
            processing_time_ms=processing_time,
            metrics=quality_result.get("metrics")
        )
