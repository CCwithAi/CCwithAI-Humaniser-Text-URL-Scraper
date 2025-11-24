"""
Test ARCHON Pipeline - End-to-End Integration Test
Tests all refactored agents with sample AI-generated text
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from parent directory BEFORE importing agents
parent_dir = Path(__file__).parent.parent
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Now safe to import agents (they need API keys from .env)
from agents.orchestrator import HumaniserOrchestrator


# Sample AI-generated texts for testing
SAMPLE_AI_TEXTS = {
    "sales": """
    Furthermore, it is important to note that our product offers exceptional value.
    Moreover, the features included are comprehensive and well-designed. Additionally,
    customer satisfaction is our top priority. In conclusion, we believe this solution
    will meet all your requirements. It is worth mentioning that the pricing structure
    is competitive in the current market.
    """,

    "journalist": """
    It seems that the recent policy changes may have significant implications. Perhaps
    the most notable aspect is the comprehensive approach taken by officials. Moreover,
    stakeholders appear to be cautiously optimistic. Furthermore, it could be argued
    that these developments represent a turning point. In conclusion, the situation
    continues to evolve and warrants careful observation.
    """
}


async def test_sales_mode():
    """Test ARCHON pipeline with sales-style AI text"""
    print("\n" + "="*80)
    print("[TEST 1] SALES MODE")
    print("="*80)

    orchestrator = HumaniserOrchestrator()
    input_text = SAMPLE_AI_TEXTS["sales"]

    print(f"\n[INPUT] AI-generated sales text:")
    print(f"{'-'*80}")
    print(input_text.strip())
    print(f"{'-'*80}")

    try:
        print("\n[RUNNING] ARCHON pipeline...")
        result = await orchestrator.process(input_text, mode="sales")

        print(f"\n[SUCCESS] TRANSFORMATION COMPLETE!")
        print(f"{'-'*80}")
        print(f"\n[RESULTS]")
        print(f"  * Quality Score: {result.quality_score:.2f}")
        print(f"  * Iterations: {result.iterations}")
        print(f"  * Processing Time: {result.processing_time_ms}ms")
        print(f"  * Mode: {result.mode}")

        if result.metrics:
            print(f"\n[METRICS]")
            print(f"  * Burstiness: {result.metrics.get('burstiness', 'N/A')}")
            print(f"  * Lexical Diversity: {result.metrics.get('lexical_diversity', 'N/A')}")
            print(f"  * Contraction Ratio: {result.metrics.get('contraction_ratio', 'N/A')}")
            print(f"  * Word Count: {result.metrics.get('word_count', 'N/A')}")
            print(f"  * Sentence Count: {result.metrics.get('sentence_count', 'N/A')}")

        print(f"\n[OUTPUT] Human-like sales text:")
        print(f"{'-'*80}")
        print(result.output_text)
        print(f"{'-'*80}")

        return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_journalist_mode():
    """Test ARCHON pipeline with journalist-style AI text"""
    print("\n" + "="*80)
    print("🧪 TEST 2: JOURNALIST MODE")
    print("="*80)

    orchestrator = HumaniserOrchestrator()
    input_text = SAMPLE_AI_TEXTS["journalist"]

    print(f"\n📝 INPUT (AI-generated journalist text):")
    print(f"{'─'*80}")
    print(input_text.strip())
    print(f"{'─'*80}")

    try:
        print("\n[RUNNING]  Running ARCHON pipeline...")
        result = await orchestrator.process(input_text, mode="journalist")

        print(f"\n[SUCCESS] TRANSFORMATION COMPLETE!")
        print(f"{'─'*80}")
        print(f"\n📊 RESULTS:")
        print(f"  * Quality Score: {result.quality_score:.2f}")
        print(f"  * Iterations: {result.iterations}")
        print(f"  * Processing Time: {result.processing_time_ms}ms")
        print(f"  * Mode: {result.mode}")

        if result.metrics:
            print(f"\n📈 METRICS:")
            print(f"  * Burstiness: {result.metrics.get('burstiness', 'N/A')}")
            print(f"  * Lexical Diversity: {result.metrics.get('lexical_diversity', 'N/A')}")
            print(f"  * Contraction Ratio: {result.metrics.get('contraction_ratio', 'N/A')}")
            print(f"  * Word Count: {result.metrics.get('word_count', 'N/A')}")
            print(f"  * Sentence Count: {result.metrics.get('sentence_count', 'N/A')}")

        print(f"\n📤 OUTPUT (Human-like journalist text):")
        print(f"{'─'*80}")
        print(result.output_text)
        print(f"{'─'*80}")

        return True

    except Exception as e:
        print(f"\n[ERROR] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_environment():
    """Test that all required environment variables are set"""
    print("\n" + "="*80)
    print("[ENV CHECK] ENVIRONMENT CHECK")
    print("="*80)

    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    }

    optional_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
    }

    all_ok = True

    print("\n[SUCCESS] Required API Keys:")
    for var, value in required_vars.items():
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  * {var}: {masked}")
        else:
            print(f"  * {var}: [ERROR] NOT SET")
            all_ok = False

    print("\n[OPTIONAL] Optional Configuration:")
    for var, value in optional_vars.items():
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  * {var}: {masked}")
        else:
            print(f"  * {var}: Not set (will use mock data)")

    return all_ok


async def main():
    """Run all ARCHON pipeline tests"""
    print("\n" + "="*80)
    print("   ARCHON PIPELINE INTEGRATION TEST - Pydantic AI Framework")
    print("="*80)

    # Test environment
    env_ok = await test_environment()

    if not env_ok:
        print("\n[WARNING]  WARNING: Required API keys not set!")
        print("Please configure .env file with OPENAI_API_KEY and ANTHROPIC_API_KEY")
        return

    # Run tests
    results = []

    # Test 1: Sales Mode
    results.append(await test_sales_mode())

    await asyncio.sleep(2)  # Brief pause between tests

    # Test 2: Journalist Mode
    results.append(await test_journalist_mode())

    # Summary
    print("\n" + "="*80)
    print("📋 TEST SUMMARY")
    print("="*80)

    passed = sum(results)
    total = len(results)

    print(f"\n  Tests Passed: {passed}/{total}")
    print(f"  Tests Failed: {total - passed}/{total}")

    if all(results):
        print("\n[SUCCESS] ALL TESTS PASSED! ARCHON pipeline is working correctly.")
    else:
        print("\n[ERROR] SOME TESTS FAILED. Check errors above for details.")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
