from serp_backbone import DatabaseManager, SerpApiSearch, UserCLI
from cachetools import LRUCache
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    try:
        db_manager = DatabaseManager()
        cache_size = int(os.getenv("CACHE_SIZE", 100))
        cache = LRUCache(maxsize=cache_size)

        api_key = os.getenv("SERP_API_KEY")
        if not api_key:
            raise ValueError("API key not found in .env file.")

        serp_api = SerpApiSearch(api_key, db_manager, cache)
        cli = UserCLI(serp_api)
        cli.run()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
