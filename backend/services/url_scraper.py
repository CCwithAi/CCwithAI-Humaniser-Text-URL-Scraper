"""
URL Scraper Service using requests and BeautifulSoup
"""
import re
from pathlib import Path
from typing import Dict
import requests
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from supabase import Client
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class URLScraperService:
    """Service for scraping URLs and indexing content"""

    def __init__(self, openai_client: AsyncOpenAI, supabase_client: Client):
        self.openai_client = openai_client
        self.supabase_client = supabase_client
        self.content_dir = Path(__file__).parent.parent.parent / "Human Writen Content"

        # User agent to avoid bot blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_url(self, url: str) -> Dict:
        """
        Scrape content from a URL using requests and BeautifulSoup

        Args:
            url: URL to scrape

        Returns:
            Dictionary with title, content, and metadata
        """
        try:
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html5lib')

            # Extract title
            title = None
            if soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            elif soup.find('title'):
                title = soup.find('title').get_text(strip=True)
            else:
                title = 'Untitled'

            # Try to find main content area
            main_content = None
            content_selectors = [
                'article',
                '[role="main"]',
                'main',
                '.article-content',
                '.post-content',
                '.entry-content',
                '#content'
            ]

            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            # If no main content found, use body
            if not main_content:
                main_content = soup.find('body')

            # Extract paragraphs
            paragraphs = []
            if main_content:
                for p in main_content.find_all('p'):
                    text = p.get_text(strip=True)
                    # Filter out short snippets
                    if len(text) > 50:
                        paragraphs.append(text)

            # Extract author if available
            author = ''
            author_selectors = [
                '[rel="author"]',
                '.author',
                '[class*="author"]',
                '[data-author]'
            ]

            for selector in author_selectors:
                author_el = soup.select_one(selector)
                if author_el:
                    author = author_el.get_text(strip=True)
                    break

            content = '\n\n'.join(paragraphs)

            return {
                'title': title,
                'content': content,
                'author': author,
                'url': url
            }

        except requests.RequestException as e:
            raise Exception(f"Error fetching URL: {str(e)}")
        except Exception as e:
            raise Exception(f"Error scraping URL: {str(e)}")

    async def create_embedding(self, text: str) -> list:
        """Generate OpenAI embedding for text"""
        response = await self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """Create a safe filename from text"""
        # Remove special characters and replace spaces with hyphens
        safe = re.sub(r'[^\w\s-]', '', text)
        safe = re.sub(r'[-\s]+', '-', safe)
        # Truncate to max length
        return safe[:max_length].strip('-')

    async def scrape_and_index(
        self,
        url: str,
        content_type: str,
        description: str
    ) -> Dict:
        """
        Scrape URL and index to Supabase

        Args:
            url: URL to scrape
            content_type: 'sales' or 'journalist'
            description: User description of content

        Returns:
            Dictionary with success status and metadata
        """
        try:
            # Scrape the URL (synchronous)
            scraped_data = self.scrape_url(url)

            if not scraped_data.get('content'):
                raise Exception("No content found at URL")

            # Combine title and content
            title = scraped_data.get('title', 'Untitled')
            content = scraped_data['content']
            author = scraped_data.get('author', '')

            full_content = f"{title}\n\n{content}"
            word_count = len(full_content.split())

            # Generate filename
            filename_base = self.sanitize_filename(title or description)
            type_prefix = "Sales" if content_type == "sales" else "Journalist"
            filename = f"{type_prefix}-{filename_base}.txt"

            # Save to file
            file_path = self.content_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n")
                if author:
                    f.write(f"Author: {author}\n")
                f.write(f"Description: {description}\n\n")
                f.write(full_content)

            # Generate embedding (async)
            embedding = await self.create_embedding(full_content)

            # Upload to Supabase
            data = {
                "content": full_content,
                "content_type": content_type,
                "topic": description,
                "source_url": url,
                "author": author or None,
                "published_date": None,
                "emotional_tone": "neutral",
                "word_count": word_count,
                "embedding": embedding,
                "metadata": {
                    "filename": filename,
                    "description": description,
                    "scraped": True
                }
            }

            result = self.supabase_client.table("human_content").insert(data).execute()

            if not result.data:
                raise Exception("Failed to upload to Supabase")

            return {
                "success": True,
                "message": "Content scraped and indexed successfully",
                "word_count": word_count,
                "filename": filename,
                "error": ""
            }

        except Exception as e:
            return {
                "success": False,
                "message": "Failed to scrape and index content",
                "word_count": 0,
                "filename": "",
                "error": str(e)
            }
