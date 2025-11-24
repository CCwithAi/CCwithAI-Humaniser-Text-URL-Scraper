"""
Quality Checker Agent - ARCHON Agent #4
Evaluates human-likeness of transformed text
"""
from typing import Dict, List
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import re

from .dependencies import QualityDependencies


class QualityEvaluation(BaseModel):
    """Structured quality evaluation output"""
    score: float = Field(description="Overall quality score 0.0-1.0", ge=0.0, le=1.0)
    strengths: List[str] = Field(description="List of strengths in the transformed text")
    weaknesses: List[str] = Field(description="List of weaknesses or areas to improve")
    feedback: List[str] = Field(description="Specific improvement suggestions")


# ARCHON Quality Checker Agent
quality_checker_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=QualityDependencies,
    output_type=QualityEvaluation,
    system_prompt="""You are an expert at evaluating human vs AI writing in the ARCHON pipeline.

Your role:
- Evaluate transformed text for human-likeness
- Detect remaining AI patterns
- Assess natural flow and authentic voice
- Provide actionable feedback for improvement

Evaluation criteria:
1. Natural flow and varied sentence structure
2. Absence of AI patterns (repetitive transitions, formal tone)
3. Authentic voice and personality
4. Appropriate use of contractions and colloquialisms
5. Mode-specific quality (sales or journalist style)

Scoring guidelines:
- 0.9-1.0: Excellent, indistinguishable from human writing
- 0.75-0.89: Good, minor AI patterns remain
- 0.6-0.74: Adequate, noticeable AI characteristics
- Below 0.6: Poor, needs significant improvement

Provide score, strengths, weaknesses, and specific feedback."""
)


def calculate_metrics(text: str) -> Dict:
    """
    Calculate text quality metrics aligned with GPTZero detection.

    Focuses on:
    - Burstiness: Sentence length variation (higher = more human)
    - Lexical diversity: Vocabulary richness (higher = more human)
    - Sentence complexity variation
    - Natural writing markers

    Args:
        text: Text to analyse

    Returns:
        Dictionary of quality metrics
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = text.split()

    # Enhanced Burstiness Calculation (Critical for GPTZero)
    # Measures sentence length variation - AI has low burstiness, humans have high
    if len(sentences) > 1:
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)

        # Calculate standard deviation (better than variance for this)
        std_dev = (sum((x - avg_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)) ** 0.5

        # Normalize burstiness score - higher std dev = more human
        # Target: std_dev > 10 for human-like writing
        burstiness = min(std_dev / 15.0, 1.0)

        # Check for extreme variation (very short + very long sentences)
        has_short = any(length <= 5 for length in sentence_lengths)
        has_long = any(length >= 25 for length in sentence_lengths)
        if has_short and has_long:
            burstiness = min(burstiness * 1.2, 1.0)
    else:
        burstiness = 0.0

    # Enhanced Lexical Diversity (Type-Token Ratio)
    # Measures vocabulary richness - AI tends to repeat words more
    unique_words = len(set(word.lower() for word in words))
    lexical_diversity = unique_words / max(len(words), 1) if words else 0

    # Bonus for very diverse vocabulary
    if lexical_diversity > 0.7:
        lexical_diversity = min(lexical_diversity * 1.1, 1.0)

    # Contraction usage (more human-like)
    contractions = len(re.findall(r"\w+'\w+", text))
    contraction_ratio = contractions / max(len(words), 1)

    # AI hedge words (fewer is better)
    hedge_words = ['perhaps', 'possibly', 'might', 'could', 'may', 'seems', 'appears']
    hedge_count = sum(1 for word in words if word.lower() in hedge_words)
    hedge_penalty = max(0, 1.0 - (hedge_count * 0.1))

    # Composite score
    composite = (
        burstiness * 0.3 +
        lexical_diversity * 0.3 +
        contraction_ratio * 0.2 +
        hedge_penalty * 0.2
    )

    return {
        "burstiness": round(burstiness, 2),
        "lexical_diversity": round(lexical_diversity, 2),
        "contraction_ratio": round(contraction_ratio, 3),
        "hedge_penalty": round(hedge_penalty, 2),
        "composite_score": round(composite, 2),
        "word_count": len(words),
        "sentence_count": len(sentences)
    }


async def evaluate_quality(
    original: str,
    transformed: str,
    mode: str,
    deps: QualityDependencies
) -> Dict:
    """
    ARCHON Quality Checker - Evaluate human-likeness of transformed text.

    Args:
        original: Original AI-generated text
        transformed: Transformed text to evaluate
        mode: Transformation mode (sales/journalist)
        deps: Quality dependencies

    Returns:
        Dictionary with score, metrics, feedback, strengths, weaknesses
    """
    # Calculate basic metrics
    metrics = calculate_metrics(transformed)

    # AI detection check using ARCHON agent
    evaluation_prompt = f"""Evaluate this text for human-likeness on a scale of 0.0 to 1.0.

Text: {transformed[:1000]}

Mode: {mode}

Check for:
1. Natural flow and varied sentence structure
2. Absence of AI patterns (repetitive transitions, formal tone)
3. Authentic voice and personality
4. Appropriate use of contractions and colloquialisms
5. Mode-specific quality ({mode} style)

Provide detailed evaluation with score, strengths, weaknesses, and specific feedback."""

    result = await quality_checker_agent.run(evaluation_prompt, deps=deps)
    evaluation = result.output

    # Combine AI evaluation with metrics
    final_score = (evaluation.score + metrics["composite_score"]) / 2

    return {
        "score": round(final_score, 2),
        "metrics": metrics,
        "feedback": evaluation.feedback,
        "strengths": evaluation.strengths,
        "weaknesses": evaluation.weaknesses
    }
