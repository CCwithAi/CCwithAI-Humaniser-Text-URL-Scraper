"""
Content Retrieval Agent - ARCHON Agent #2
Manages human content database and retrieves relevant examples
"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from .dependencies import RetrievalDependencies


class HumanContentExample(BaseModel):
    """Structured human content example"""
    content: str
    source: str
    content_type: Optional[str] = None
    topic: Optional[str] = None
    similarity: Optional[float] = None


# ARCHON Content Retrieval Agent
content_retrieval_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=RetrievalDependencies,
    system_prompt="""You are an expert at managing and retrieving human-written content samples in the ARCHON pipeline.

Your role:
- Retrieve relevant human writing examples from the database
- Match content type (sales vs journalist) and topic
- Provide high-quality reference material for style transformation

Content types:
- journalist: Objective reporting, news articles, editorial content
- sales: Marketing copy, persuasive writing, promotional content"""
)


async def search_vector_database(
    deps: RetrievalDependencies,
    embedding: List[float],
    content_type: str,
    limit: int = 5
) -> List[Dict]:
    """
    Search Supabase vector database for similar human content.

    Args:
        deps: Retrieval dependencies with Supabase client
        embedding: Query embedding vector
        content_type: Filter by content type (sales/journalist)
        limit: Maximum number of results

    Returns:
        List of matching human content examples
    """
    if not deps.supabase_enabled or not deps.supabase_client:
        return []

    try:
        result = deps.supabase_client.rpc(
            'match_human_content',
            {
                'query_embedding': embedding,
                'match_count': limit,
                'content_type_filter': content_type
            }
        ).execute()

        return result.data if result.data else []
    except Exception as e:
        print(f"Vector search error: {e}")
        return []


async def get_filtered_content(
    deps: RetrievalDependencies,
    content_type: str,
    limit: int = 5
) -> List[Dict]:
    """
    Retrieve human content filtered by type (fallback when no embedding).

    Args:
        deps: Retrieval dependencies with Supabase client
        content_type: Content type filter
        limit: Maximum number of results

    Returns:
        List of human content examples
    """
    if not deps.supabase_enabled or not deps.supabase_client:
        return []

    try:
        result = deps.supabase_client.table('human_content')\
            .select('*')\
            .eq('content_type', content_type)\
            .limit(limit)\
            .execute()

        return result.data if result.data else []
    except Exception as e:
        print(f"Filtered query error: {e}")
        return []


def get_mock_examples(content_type: str) -> List[Dict]:
    """
    Provide mock examples when Supabase is unavailable.

    Args:
        content_type: Type of content needed

    Returns:
        List of mock human writing examples
    """
    if content_type == "journalist":
        return [
            {
                "content": "Local residents gathered today to protest the proposed development. The crowd, numbering around 200, voiced concerns about increased traffic and environmental impact. 'We're not against progress,' said Sarah Mitchell, a local teacher. 'But this feels rushed.' Council representatives promised to review the feedback before next month's decision.",
                "source": "Mock Local News",
                "content_type": "journalist",
                "topic": "local_news"
            }
        ]
    else:  # sales
        return [
            {
                "content": "You're going to love this. We've slashed prices by 40% and thrown in free delivery. No catches, no hidden fees. Just brilliant value that'll make you smile. Grab yours before they're gone – this deal won't last forever.",
                "source": "Mock Sales Copy",
                "content_type": "sales",
                "topic": "promotion"
            }
        ]


async def retrieve_human_content(
    content_type: str,
    topic: str,
    embedding: Optional[List[float]],
    deps: RetrievalDependencies,
    limit: int = 5
) -> List[Dict]:
    """
    ARCHON Content Retrieval - Get relevant human writing examples.

    Args:
        content_type: 'sales' or 'journalist'
        topic: Content topic for filtering
        embedding: Vector embedding for similarity search
        deps: Retrieval dependencies with Supabase client
        limit: Number of examples to retrieve

    Returns:
        List of human content examples
    """
    # Try vector search if embedding provided and Supabase available
    if embedding and deps.supabase_enabled:
        results = await search_vector_database(
            deps=deps,
            embedding=embedding,
            content_type=content_type,
            limit=limit
        )
        if results:
            return results

    # Fallback to filtered query
    if deps.supabase_enabled:
        results = await get_filtered_content(
            deps=deps,
            content_type=content_type,
            limit=limit
        )
        if results:
            return results

    # Final fallback to mock data
    return get_mock_examples(content_type)
