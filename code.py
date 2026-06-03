from typing import Any, Dict, List, Optional, Union
from db.sql_client import SQL_DB
from db.sql_queries import *


class Client:
    def __init__(self, DATABASE: SQL_DB) -> None:
        """
        Initializes the business logic Client with a connected SQL database engine instance.
        :param DATABASE: An instance of the SQL_DB class used to execute queries.
        """
        self.DATABASE: SQL_DB = DATABASE


    def search_film_with_keyword(self, keyword: str, limit: int = 10, off_set: int = 0) -> List[Dict[str, Any]]:
        """
        Searches for movies containing the specified keyword in their title with pagination support.
        :param keyword: The raw search string or phrase provided by the user.
        :param limit: Maximum number of movie records to fetch per page.
        :param off_set: SQL pagination offset indicating how many records to skip.
        :return: A list of dictionaries representing the found movie records.
        """
        keyword = f'%{keyword}%'
        return self.DATABASE.select(SEARCH_FILM_BY_TITLE, (keyword, limit, off_set))


    def show_all_categories(self) -> List[Dict[str, Any]]:
        """
        Fetches the complete list of all available movie categories/genres from the database.
        :return: A list of dictionaries containing available category names.
        """
        return self.DATABASE.select(SHOW_ALL_CATEGORIES)


    def minimal_year_for_film(self) -> List[Dict[str, Any]]:
        """
        Retrieves the oldest (minimum) movie release year stored in the database.
        :return: A list containing a single row dictionary with the minimum year.
        """
        return self.DATABASE.select(MINIMAL_YEAR_FOR_FILM)


    def maximal_year_for_film(self) -> List[Dict[str, Any]]:
        """
        Retrieves the newest (maximum) movie release year stored in the database.
        :return: A list containing a single row dictionary with the maximum year.
        """
        return self.DATABASE.select(MAXIMAL_YEAR_FOR_FILM)


    def search_film_by_category(self, category: str, limit: int = 10, off_set: int = 0) -> List[Dict[str, Any]]:
        """
        Filters and retrieves movies belonging to a specific genre/category name with pagination.
        :param category: The exact name of the category to filter by.
        :param limit: Maximum number of movie records to fetch per page.
        :param off_set: SQL pagination offset indicating how many records to skip.
        :return: A list of dictionaries representing the filtered movie records.
        """
        return self.DATABASE.select(SEARCH_FILM_BY_CATEGORY, (category, limit, off_set))


    def search_film_by_year(self, year: int, limit: int = 10, off_set: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieves movies released in a specific single calendar year with pagination.
        :param year: The target release year to filter by.
        :param limit: Maximum number of movie records to fetch per page.
        :param off_set: SQL pagination offset indicating how many records to skip.
        :return: A list of dictionaries representing the movie records for that year.
        """
        return self.DATABASE.select(SEARCH_FILM_BY_YEAR, (year, limit, off_set))


    def search_film_by_years_range(self, year_min: int, year_max: int, limit: int = 10, off_set: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieves movies released within a specific time period range (inclusive boundaries) with pagination.
        :param year_min: The starting year boundary (FROM).
        :param year_max: The ending year boundary (TO).
        :param limit: Maximum number of movie records to fetch per page.
        :param off_set: SQL pagination offset indicating how many records to skip.
        :return: A list of dictionaries representing the movie records within the period interval.
        """
        return self.DATABASE.select(SEARCH_FILM_BY_YEAR_RANGE, (year_min, year_max, limit, off_set))
