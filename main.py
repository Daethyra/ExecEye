from serp_backbone import DatabaseManager, SerpApiSearch, UserCLI
from cachetools import LRUCache
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

def main():
    try:
        # Initialize database manager
        db_manager = DatabaseManager()

        # Initialize cache
        cache_size = int(os.getenv("CACHE_SIZE", 100))  # Default to 100 if not set
        cache = LRUCache(maxsize=cache_size)

        # Initialize the SerpApiSearch class
        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env file.")
        
        serp_api = SerpApiSearch(api_key, db_manager, cache)

        # Initialize the CLI
        cli = UserCLI(serp_api)

        # Run the CLI
        cli.run()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
