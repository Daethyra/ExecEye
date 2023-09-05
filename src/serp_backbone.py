"""
SerpAPI Search with Asynchronous Database Management and CLI Interface
"""

# Standard Libraries
import os
import logging
import asyncio
from typing import Union, List, Dict, Optional
from contextlib import asynccontextmanager

# Third-Party Libraries
from serpapi import GoogleSearch
from dotenv import load_dotenv
from cachetools import LRUCache
import aiosqlite

# Initialize logging and environment variables
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

def get_env_variable(var_name: str) -> Optional[str]:
    """Get the value of an environment variable."""
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f"{var_name} not set in environment.")
        return None

class AsyncDatabaseManager:
    """Asynchronous Database Manager."""
    _instance = None
    MAX_POOL_SIZE = 10
    connection_pool: List[aiosqlite.Connection] = []

    def __new__(cls) -> 'AsyncDatabaseManager':
        if cls._instance is None:
            cls._instance = super(AsyncDatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Database Manager and run the asynchronous database setup."""
        asyncio.run(self.init_db())

    async def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        try:
            if len(self.connection_pool) < self.MAX_POOL_SIZE:
                self.conn = await aiosqlite.connect("async_serp_results.db")
                self.connection_pool.append(self.conn)
            else:
                self.conn = self.connection_pool.pop(0)
            
            self.cursor = await self.conn.cursor()
            await self.create_tables()
            self.connection_pool.append(self.conn)
            logging.info("Async database initialized successfully.")
        except Exception as e:
            logging.error(f"Exception in async init_db: {e}")
            raise e

    async def create_tables(self):
        """Create tables for storing search results."""
        try:
            await self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    title TEXT,
                    link TEXT,
                    snippet TEXT
                )
            """)
            await self.conn.commit()
        except Exception as e:
            logging.error(f"Exception in async create_tables: {e}")
            raise e

@asynccontextmanager
async def get_async_db_connection():
    """Context manager for asynchronous database operations."""
    db = AsyncDatabaseManager()
    try:
        yield db
    finally:
        if db.conn:
            await db.conn.close()

class SerpApiSearch:
    """Perform searches using SerpAPI."""
    def __init__(self, api_key: str, cache: LRUCache):
        """Initialize with API key and cache."""
        self.api_key = api_key
        self.cache = cache

    async def search_leadership(self, company_name: str) -> Union[List[Dict], None]:
        """Search for company leadership information."""
        cache_key = f"{company_name}_leadership"
        if cache_key in self.cache:
            logging.debug("Cache hit.")
            return self.cache[cache_key]

        params = {
            "q": f"{company_name} executives OR {company_name} board of directors",
            "api_key": self.api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", None)

        if results:
            self.cache[cache_key] = results
            async with get_async_db_connection() as db:
                await db.insert_data(cache_key, str(results))

        logging.debug("Search completed.")
        return results

class UserCLI:
    """User Command Line Interface for interacting with SerpAPI Search."""
    def __init__(self, searcher: SerpApiSearch):
        """Initialize CLI with the searcher object."""
        self.searcher = searcher

    async def run(self):
        """Run the CLI loop for user input and display search results."""
        try:
            while True:
                company_name = input("Enter the company name to search for leadership: ")
                if not company_name:
                    print("Company name cannot be empty.")
                    continue
                
                # Ensure that input is sanitized, for security reasons
                company_name = company_name.strip()

                results = await self.searcher.search_leadership(company_name)
                if results:
                    print(f"\nExecutives found for {company_name}:")
                    for i, result in enumerate(results):
                        title = result.get('title', 'N/A')
                        link = result.get('link', 'N/A')
                        snippet = result.get('snippet', 'N/A')
                        print(f"  - {title}\n    Link: {link}\n    Snippet: {snippet}\n")
                else:
                    print(f"No executives found for {company_name}.")
                    
        except KeyboardInterrupt:
            print("\nExiting program. Goodbye!")

# Initialize and run the CLI
if __name__ == "__main__":
    api_key = get_env_variable("SERP_API_KEY")
    if not api_key:
        logging.error("API key is missing. Exiting.")
        exit(1)

    db_manager = AsyncDatabaseManager()
    cache = LRUCache(maxsize=100)
    searcher = SerpApiSearch(api_key=api_key, cache=cache)
    cli = UserCLI(searcher)
    asyncio.run(cli.run())
