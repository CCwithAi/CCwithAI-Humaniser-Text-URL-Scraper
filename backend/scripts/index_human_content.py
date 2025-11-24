"""
Index Human Content to Supabase
Reads human-written content files and uploads them to Supabase with embeddings
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from supabase import create_client, Client
import re

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
load_dotenv(dotenv_path=parent_dir / ".env")

# Initialize clients
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

CONTENT_DIR = parent_dir / "Human Writen Content"


def detect_content_type(filename: str) -> str:
    """Detect content type from filename"""
    filename_lower = filename.lower()

    if "news" in filename_lower or "journalist" in filename_lower or "article" in filename_lower:
        return "journalist"
    elif "sales" in filename_lower or "marketing" in filename_lower:
        return "sales"
    elif "blog" in filename_lower:
        return "blog"
    elif "social" in filename_lower:
        return "social_media"
    else:
        return "general"


def extract_topic(content: str, content_type: str) -> str:
    """Extract topic from content"""
    # Get first 200 characters and extract key nouns/topics
    first_lines = content[:200].strip()

    # Simple topic extraction based on content type
    if content_type == "journalist":
        # Look for proper nouns and key phrases in news
        if "Lancashire" in content:
            return "Local Government"
        elif "Council" in content:
            return "Politics"
    elif content_type == "sales":
        if "bathroom" in content.lower():
            return "Home Improvement"
        elif "showroom" in content.lower():
            return "Retail"

    return "General"


def detect_emotional_tone(content: str) -> str:
    """Detect emotional tone of the content"""
    content_lower = content.lower()

    # Positive indicators
    positive_words = ["exceptional", "award winning", "exciting", "dream", "inspire", "superior"]
    # Neutral indicators
    neutral_words = ["council", "government", "proposal", "meeting", "authority"]
    # Formal indicators
    formal_words = ["furthermore", "moreover", "however", "therefore"]

    positive_count = sum(1 for word in positive_words if word in content_lower)
    neutral_count = sum(1 for word in neutral_words if word in content_lower)
    formal_count = sum(1 for word in formal_words if word in content_lower)

    if positive_count > 3:
        return "positive"
    elif formal_count > 2 or neutral_count > 5:
        return "formal"
    else:
        return "neutral"


async def create_embedding(text: str) -> list[float]:
    """Generate OpenAI embedding for text"""
    print(f"  Generating embedding...")
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


async def index_file(file_path: Path):
    """Index a single file to Supabase"""
    print(f"\n[FILE] Processing: {file_path.name}")

    # Read content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        print(f"  [WARN] Skipping empty file")
        return

    # Extract metadata
    content_type = detect_content_type(file_path.name)
    topic = extract_topic(content, content_type)
    word_count = len(content.split())
    emotional_tone = detect_emotional_tone(content)

    print(f"  Type: {content_type}")
    print(f"  Topic: {topic}")
    print(f"  Words: {word_count}")
    print(f"  Tone: {emotional_tone}")

    # Generate embedding
    embedding = await create_embedding(content)

    # Prepare data for Supabase
    data = {
        "content": content,
        "content_type": content_type,
        "topic": topic,
        "source_url": None,
        "author": None,
        "published_date": None,
        "emotional_tone": emotional_tone,
        "word_count": word_count,
        "embedding": embedding,
        "metadata": {
            "filename": file_path.name,
            "indexed_at": "auto"
        }
    }

    # Upload to Supabase
    print(f"  -> Uploading to Supabase...")
    result = supabase.table("human_content").insert(data).execute()

    if result.data:
        print(f"  [SUCCESS] Indexed successfully!")
    else:
        print(f"  [ERROR] Failed to upload")


async def main():
    """Main indexing process"""
    print("="*60)
    print("HUMAN CONTENT INDEXING SCRIPT")
    print("="*60)

    # Verify environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY not found in .env")
        return

    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("[ERROR] Supabase credentials not found in .env")
        return

    print(f"\n[SCAN] Scanning directory: {CONTENT_DIR}")

    # Find all .txt files
    txt_files = list(CONTENT_DIR.glob("*.txt"))

    if not txt_files:
        print(f"[WARN] No .txt files found in {CONTENT_DIR}")
        return

    print(f"[INFO] Found {len(txt_files)} file(s) to index\n")

    # Index each file
    for file_path in txt_files:
        try:
            await index_file(file_path)
        except Exception as e:
            print(f"  [ERROR] Error: {str(e)}")

    print("\n" + "="*60)
    print("[COMPLETE] Indexing complete!")
    print("="*60)

    # Show summary
    print("\n[SUMMARY] Database Summary:")
    result = supabase.table("human_content").select("content_type", count="exact").execute()
    print(f"   Total records: {result.count if hasattr(result, 'count') else 'N/A'}")

    # Group by content type
    result = supabase.table("human_content").select("content_type").execute()
    if result.data:
        types = {}
        for row in result.data:
            ct = row.get('content_type', 'unknown')
            types[ct] = types.get(ct, 0) + 1

        print("\n   By content type:")
        for content_type, count in types.items():
            print(f"     - {content_type}: {count}")


if __name__ == "__main__":
    asyncio.run(main())
