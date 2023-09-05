""" Start the application. """
from src.serp_backbone import AsyncDatabaseManager, SerpApiSearch, UserCLI
from cachetools import LRUCache
from dotenv import load_dotenv
import os

# Initialize the .env file.
load_dotenv()

def main():
    try:
        # Initialize the database manager, cache, and SerpApiSearch object.
        db_manager = AsyncDatabaseManager()
        cache_size = int(os.getenv("CACHE_SIZE", 100))
        cache = LRUCache(maxsize=cache_size)

        # Get the API key from the .env file.
        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env file.")

        # Initialize the CLI and run it.
        serp_api = SerpApiSearch(api_key, db_manager, cache)
        cli = UserCLI(serp_api)
        cli.run()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
