import logging
import sqlite3
from serpapi import GoogleSearch
from typing import List, Dict, Union
from cachetools import LRUCache
import os
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize environment variables
load_dotenv()


# Database manager class
class DatabaseManager:
    """
    Handles database operations.
    """
    def __init__(self):
        self.init_db()

    def init_db(self):
        try:
            self.conn = sqlite3.connect("serp_results.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    query TEXT,
                    result TEXT
                )
            """)
            self.conn.commit()
            logging.debug("Database initialized.")
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")

    def save_to_db(self, query: str, result: str):
        try:
            self.cursor.execute("INSERT INTO results (query, result) VALUES (?, ?)", (query, result))
            self.conn.commit()
            logging.debug("Saved result to database.")
        except Exception as e:
            logging.error(f"Failed to save result to database: {e}")


class SerpApiSearch:
    """
    Handles all SERP functionality.
    """
    def __init__(self, db_manager: DatabaseManager, cache: LRUCache):
        self.api_key = os.getenv("SERP_API_KEY")  # Read API key from .env
        self.db_manager = db_manager
        self.cache = cache

    def search_leadership(self, company_name: str) -> Union[List[Dict], None]:
        try:
            # Create a cache key based on the company name and search terms
            cache_key = f"{company_name}_leadership"

            if cache_key in self.cache:
                logging.debug("Cache hit.")
                return self.cache[cache_key]

            # Broaden the search to include executives and board of directors
            params = {
                "q": f"{company_name} executives OR {company_name} board of directors",
                "api_key": self.api_key
            }
            search = GoogleSearch(params)
            results = search.get_dict().get("organic_results", None)

            self.cache[cache_key] = results
            self.db_manager.save_to_db(cache_key, str(results))

            logging.debug("Search completed.")
            return results
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return None


# Command Line Interface class
class UserCLI:
    """
    Handles the Command Line Interface for the user.
    """

    def __init__(self, searcher: SerpApiSearch):
        self.searcher = searcher

    def run(self):
        while True:
            company_name = input("Enter the company name to search for leadership: ")
            results = self.searcher.search_leadership(company_name)
            if results:
                print(f"Executives found for {company_name}: {results}")
            else:
                print(f"No executives found for {company_name}.")


# Unit Tests
def test_search_leadership():
    db_manager = DatabaseManager()
    cache = LRUCache(maxsize=100)
    serp_api = SerpApiSearch(db_manager, cache)
    result = serp_api.search_leadership("Google")
    assert result is not None, "Test Failed: No leadership found."

if __name__ == "__main__":
    db_manager = DatabaseManager()
    cache = LRUCache(maxsize=100)
    serp_api = SerpApiSearch(db_manager, cache)
    cli = UserCLI(serp_api)
    cli.run()