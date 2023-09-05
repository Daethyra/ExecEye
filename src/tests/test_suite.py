""" This module contains the test suite for the ExecEye project. It is meant to be run with the command 'python -m unittest' from the ExecEye/src directory. """
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from serp_backbone import AsyncDatabaseManager, SerpApiSearch, UserCLI as sb

class TestAsyncDatabaseManager(unittest.TestCase):

    @patch("aiosqlite.connect")
    async def test_init_db(self, mock_connect):
        mock_connect.return_value = MagicMock()
        db_manager = sb.AsyncDatabaseManager()
        await db_manager.init_db()
        mock_connect.assert_called_with("async_serp_results.db")

    # Add more functions to TestAsyncDatabaseManager
    async def test_insert_data(self, mock_cursor):
        mock_cursor.execute.return_value = MagicMock()
        db_manager = sb.AsyncDatabaseManager()
        await db_manager.insert_data("fake_data")
        mock_cursor.execute.assert_called_with("INSERT INTO async_serp_results VALUES (?)", ("fake_data",))

    async def test_get_data(self, mock_cursor):
        mock_cursor.fetchall.return_value = MagicMock()
        db_manager = sb.AsyncDatabaseManager()
        await db_manager.get_data()
        mock_cursor.execute.assert_called_with("SELECT * FROM async_serp_results")
        
    async def test_update_data(self, mock_cursor):
        mock_cursor.execute.return_value = MagicMock()
        db_manager = sb.AsyncDatabaseManager()
        await db_manager.update_data("fake_data")
        mock_cursor.execute.assert_called_with("UPDATE async_serp_results SET data=? WHERE id=?", ("fake_data",))

    async def test_delete_data(self, mock_cursor):
        mock_cursor.execute.return_value = MagicMock()
        db_manager = sb.AsyncDatabaseManager()
        await db_manager.delete_data("fake_data")
        mock_cursor.execute.assert_called_with("DELETE FROM async_serp_results WHERE data=?", ("fake_data",))

class TestSerpApiSearch(unittest.TestCase):

    @patch("GoogleSearch.get_dict")
    async def test_search_leadership(self, mock_get_dict):
        mock_get_dict.return_value = {"organic_results": "some_results"}
        db_manager = MagicMock()
        cache = MagicMock()
        searcher = sb.SerpApiSearch("fake_api_key", db_manager, cache)
        result = await searcher.search_leadership("fake_company")
        self.assertEqual(result, "some_results")
    
    async def test_search_images(self, mock_get_dict):
        mock_get_dict.return_value = {"image_results": "some_results"}
        db_manager = MagicMock()
        cache = MagicMock()
        searcher = sb.SerpApiSearch("fake_api_key", db_manager, cache)
        result = await searcher.search_images("fake_company")
        self.assertEqual(result, "some_results")
        
    async def test_search_videos(self, mock_get_dict):
        mock_get_dict.return_value = {"video_results": "some_results"}
        db_manager = MagicMock()
        cache = MagicMock()
        searcher = sb.SerpApiSearch("fake_api_key", db_manager, cache)
        result = await searcher.search_videos("fake_company")
        self.assertEqual(result, "some_results")

    async def test_search_news(self, mock_get_dict):
        mock_get_dict.return_value = {"news_results": "some_results"}
        db_manager = MagicMock()
        cache = MagicMock()
        searcher = sb.SerpApiSearch("fake_api_key", db_manager, cache)
        result = await searcher.search_news("fake_company")
        self.assertEqual(result, "some_results")

class TestUserCLI(unittest.TestCase):

    @patch("builtins.input", lambda *_: "fake_company")
    @patch("sb.SerpApiSearch.search_leadership")
    async def test_run_with_multiple_results(self, mock_search_leadership):
        mock_search_leadership.return_value = [{"title": "CEO", "link": "some_link", "snippet": "some_snippet"}, 
                                            {"title": "CFO", "link": "some_other_link", "snippet": "some_other_snippet"}]
        searcher = MagicMock()
        cli = sb.UserCLI(searcher)
        await cli.run()  # This should be run in a way that it can be stopped after one iteration to prevent infinite loop


    @patch("builtins.input", lambda *_: "fake_company")
    @patch("sb.SerpApiSearch.search_leadership")
    async def test_run_with_no_results(self, mock_search_leadership):
        mock_search_leadership.return_value = []
        searcher = MagicMock()
        cli = sb.UserCLI(searcher)
        await cli.run()  # This should be run in a way that it can be stopped after one iteration to prevent infinite loop


    @patch("builtins.input", lambda *_: "fake_company")
    @patch("sb.SerpApiSearch.search_leadership")
    async def test_run_with_invalid_input(self, mock_search_leadership):
        mock_search_leadership.return_value = []
        searcher = MagicMock()
        cli = sb.UserCLI(searcher)
        with self.assertRaises(ValueError):
            await cli.run()  # This should be run in a way that it can be stopped after one iteration to prevent infinite loop

if __name__ == "__main__":
    unittest.main()
