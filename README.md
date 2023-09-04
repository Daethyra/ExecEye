# ExecEye - A Harvest of Corporate Leadership's Names

## Overview

This project aims to provide a command-line interface for searching company leadership information using the SerpAPI. It also includes caching and database storage functionalities to improve performance and persist results.
The database schema has been optimized to store only relevant information such as the executive's title, link to the source, and a snippet. Additionally, the CLI output has been formatted for better readability.

## Dependencies

* Python 3.x
* `google-search-results` (SerpAPI)
* `cachetools`
* `python-dotenv`

## Installation

1. Clone the repository.
2. Install the required packages.
3. Rename the `.env.template` to `.env`, then add your SerpAPI key:value for `SERP_API_KEY=`.

## Modules

### `DatabaseManager`

#### Responsibilities

* Initializes and manages the SQLite database.
* Saves search results to the database.

#### Methods

* `init_db()`: Initializes the database.
* `save_to_db(query: str, result: str)`: Saves a query and its result to the database.

### `SerpApiSearch`

#### Responsibilities

* Performs searches using SerpAPI.
* Caches results using LRU Cache.
* Saves results to the database.

#### Methods

* `search_leadership(company_name: str) -> Union[List[Dict], None]`: Searches for leadership information of a given company.

### `UserCLI`

#### Responsibilities

* Provides a command-line interface for the user to input company names.
* Displays search results.

#### Methods

* `run()`: Runs the CLI loop, allowing the user to input company names and displaying search results.

## Unit Tests

* `test_search_leadership()`: Tests the `search_leadership` method of the `SerpApiSearch` class.

## Usage

Run `main.py` to start the application. Follow the on-screen instructions to search for company leadership information.
--------------------------------------------------------------------------------------------------------------
