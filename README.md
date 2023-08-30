# SERP Search and Cache Project

## Overview

This project aims to provide a command-line interface for searching company leadership information using the SerpAPI. It also includes caching and database storage functionalities to improve performance and persist results.

## Dependencies

* Python 3.x
* `serpapi`
* `sqlite3`
* `cachetools`
* `python-dotenv`

## Installation

1. Clone the repository.
2. Install the required packages.
3. Create a copy of the `.env.template` file and add your SerpAPI key as `SERP_API_KEY=your_key_here`.

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
