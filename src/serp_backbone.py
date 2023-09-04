import logging
import sqlite3
from serpapi import GoogleSearch
from typing import List, Dict, Union
from cachetools import LRUCache
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.init_db()

    def init_db(self):
        try:
            self.conn = sqlite3.connect("serp_results.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    query TEXT,
                    title TEXT,
                    link TEXT,
                    snippet TEXT
                )
            """)
            self.conn.commit()
            logging.debug("Database initialized.")
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")

    def save_to_db(self, query: str, results: List[Dict]):
        try:
            for result in results:
                title = result.get('title', '')
                link = result.get('link', '')
                snippet = result.get('snippet', '')
                self.cursor.execute(
                    "INSERT INTO results (query, title, link, snippet) VALUES (?, ?, ?, ?)",
                    (query, title, link, snippet))
                self.conn.commit()
                logging.debug("Saved result to database.")
        except Exception as e:
            logging.error(f"Failed to save result to database: {e}")

class SerpApiSearch:
    def __init__(self, api_key: str, db_manager: DatabaseManager, cache: LRUCache):
        self.api_key = api_key
        self.db_manager = db_manager
        self.cache = cache

    def search_leadership(self, company_name: str) -> Union[List[Dict], None]:
        try:
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
                self.db_manager.save_to_db(cache_key, str(results))

            logging.debug("Search completed.")
            return results
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return None

class UserCLI:
    def __init__(self, searcher: SerpApiSearch):
        self.searcher = searcher

    def run(self):
        try:
            while True:
                company_name = input("Enter the company name to search for leadership: ")
                results = self.searcher.search_leadership(company_name)
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
            exit(0)
