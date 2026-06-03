import os
from typing import Any, Dict, List, Optional


class UI:
    def __init__(self, db_engine: Any, mongo_client: Any) -> None:
        """
        Initializes the User Interface component with MySQL and MongoDB engines.

        :param db_engine: The primary MySQL database interaction service.
        :param mongo_client: The MongoDB logger client service instance.
        """
        self.db: Any = db_engine
        self.mongo: Any = mongo_client
        self.user_current_query: Any = ""
        self.offset: int = 0
        self.limit: int = 10
        self.search_mode: str = ""
        self.year_start: Optional[int] = None
        self.year_end: Optional[int] = None

    def clear_screen(self) -> None:
        """
        Clears the terminal screen.
        Compatible with standard terminal apps and the PyCharm Run/Terminal tab.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" * 50)

    def print_banner(self) -> None:
        """
        Prints the application's decorative header banner on the screen.
        """
        title: str = "KINO_SEARCH_FILMS BY Nikita"
        print("╔" + "═" * 50 + "╗")
        print(f"║{title.center(50)}║")
        print("╚" + "═" * 50 + "╝")

    def print_menu(self) -> None:
        """
        Prints the main navigation menu items to the screen.
        """
        print("\n  MAIN MENU:")
        print("  1. 🔍 Search Movie by Title")
        print("  2. 🎭 Search Movie by Genre")
        print("  3. 📅 Search Movie by Year / Period")
        print("  4. 📊 View Search Statistics (MongoDB)")  # <-- НАША НОВАЯ КНОПКА
        print("  5. ❌ Exit")
        print("-" * 52)

    def show_results_visual(self, sql_result: List[Dict[str, Any]], current_page: int) -> None:
        """
        Renders the retrieved list of movies onto the screen with custom formatting.

        :param sql_result: List of dictionaries containing movie details from PyMySQL.
        :param current_page: The sequential number of the page currently being displayed.
        """
        print("\n" + "=" * 35)
        print(f"  SEARCH RESULTS (Page {current_page})")
        print("=" * 35)

        start_number: int = self.offset + 1

        for num, film in enumerate(sql_result, start_number):
            title: str = film.get('title', 'Unknown')
            description: str = film.get('description', 'No description available.')
            release_year: Any = film.get('release_year', 'N/A')
            length: Any = film.get('length', 'N/A')
            film_categories: str = film.get('film_categories', 'Uncategorized')

            print(f"  【{num}】 🎬 {title}")
            print(f"  📅 Year: {release_year}  |  ⏳ Duration: {length} min.")
            print(f"  🎭 Categories: {film_categories}")
            print(f"  📝 Description: {description}")
            print("-" * 60)

    @staticmethod
    def _sanitize_input(user_input: str) -> str:
        """
        Sanitizes user input to prevent wildcard exploits in SQL LIKE statements.
        Removes '%' and '_' symbols that would otherwise return all entries.

        :param user_input: The raw string provided by the user.
        :return: A safe, cleaned string for database query operations.
        """
        clean_string: str = user_input.replace("%", "").replace("_", "")
        return clean_string.strip()

    def select_and_show_genres(self) -> Optional[str]:
        """
        Fetches all available genres from the database, displays them via a for loop,
        and requests the user to make a valid selection.

        :return: The exact string name of the selected genre, or None if cancelled.
        """
        genres: Optional[List[Dict[str, Any]]] = self.db.show_all_categories()

        if not genres:
            print("\n[!] Error: Unable to load categories from the database.")
            input("\nPress Enter to return to Main Menu...")
            return None

        print("\n" + "=" * 30)
        print("     AVAILABLE CATEGORIES")
        print("=" * 30)

        for num, genre in enumerate(genres, 1):
            genre_name: str = genre.get('name') or genre.get('category_name') or 'Unknown'
            print(f"  {num}. 🎭 {genre_name}")
        print("-" * 30)

        while True:
            print("Enter 0 to return to the Main Menu.")
            user_choice: str = input("Select a category number or enter name manually: ").strip()

            if user_choice == "0":
                return None

            if not user_choice:
                print("Error: Input cannot be empty!")
                continue

            if user_choice.isdigit():
                idx: int = int(user_choice) - 1
                if 0 <= idx < len(genres):
                    selected_dict: Dict[str, Any] = genres[idx]
                    return selected_dict.get('name') or selected_dict.get('category_name')
                else:
                    print("Error: Invalid category number! Please try again.")
                    continue
            return user_choice

    def show_years_range_and_get_choice(self) -> Optional[str]:
        """
        Displays the available movie release year thresholds stored in the database
        and prompts the user to choose between single year or period range searches.

        :return: "1" for single year, "2" for a period interval, or None if cancelled.
        """
        min_year_data: Any = self.db.minimal_year_for_film()
        max_year_data: Any = self.db.maximal_year_for_film()

        min_year: Any = min_year_data[0]['release_year']
        max_year: Any = max_year_data[0]['release_year']

        print("\n" + "=" * 35)
        print("       SEARCH MOVIES BY YEAR")
        print("=" * 35)
        print(f"  Available database range: {min_year} - {max_year}")
        print("-" * 35)
        print("  1. Search by a Specific Year")
        print("  2. Search by a Time Period Range")
        print("  0. Return to Main Menu")
        print("-" * 35)

        while True:
            choice: str = input("Select an option: ").strip()
            if choice == "0":
                return None
            if choice in ("1", "2"):
                return choice
            print("[!] Invalid selection! Please enter 1, 2, or 0.")

    def start(self) -> None:
        """
        Starts the primary execution loop of the command line interface application.
        """
        while True:
            self.print_banner()
            self.print_menu()

            choice: str = input("Select an option: ").strip()

            if choice == "1":
                while True:
                    print("Enter 0 to return to the Main Menu.")
                    user_input: str = input("Enter movie title: ").strip()

                    if user_input == "0":
                        break

                    if not user_input:
                        print("Error: Movie title cannot be empty!")
                        continue

                    safe_input: str = self._sanitize_input(user_input)
                    if not safe_input:
                        print("Error: Invalid search characters entered!")
                        continue

                    self.user_current_query = safe_input
                    self.offset = 0
                    self.search_mode = "keyword"
                    self.show_results_loop()
                    break

            elif choice == "2":
                genre_choice: Optional[str] = self.select_and_show_genres()
                if genre_choice is None:
                    continue

                self.user_current_query = genre_choice
                self.offset = 0
                self.search_mode = "genre"
                self.show_results_loop()

            elif choice == "3":
                year_mode: Optional[str] = self.show_years_range_and_get_choice()
                if year_mode is None:
                    continue

                if year_mode == "1":
                    year_input: str = input("Enter the specific release year: ").strip()
                    if not year_input.isdigit():
                        print("Error: Year must be a valid numeric value!")
                        input("Press Enter to return...")
                        continue

                    self.user_current_query = int(year_input)
                    self.offset = 0
                    self.search_mode = "year_single"
                    self.show_results_loop()

                elif year_mode == "2":
                    start_input: str = input("Enter starting year (FROM): ").strip()
                    end_input: str = input("Enter ending year (TO): ").strip()

                    if not (start_input.isdigit() and end_input.isdigit()):
                        print("Error: Year boundaries must be valid numeric values!")
                        input("Press Enter to return...")
                        continue

                    self.year_start = int(start_input)
                    self.year_end = int(end_input)
                    self.offset = 0
                    self.search_mode = "year_range"
                    self.show_results_loop()

            elif choice == "4":
                self.show_statistics_menu()

            elif choice == "5":
                print("\nThe program has been successfully closed. See you next time!")
                break
            else:
                print("\n[!] Invalid selection! Please choose a valid option from the menu.")
                input("\nPress Enter to continue...")

    def show_results_loop(self) -> None:
        """
        Executes the pagination navigation loop for scrolling through movie results.
        Supports dynamic routing to different database engine methods based on the current mode.
        """
        while True:
            if self.search_mode == "keyword":
                movies: Optional[List[Dict[str, Any]]] = self.db.search_film_with_keyword(
                    self.user_current_query, self.limit, self.offset
                )
            elif self.search_mode == "genre":
                movies = self.db.show_all_categories(
                    self.user_current_query, self.limit, self.offset
                )
            elif self.search_mode == "year_single":
                movies = self.db.search_film_by_year(
                    self.user_current_query, self.limit, self.offset
                )
            elif self.search_mode == "year_range":
                movies = self.db.search_film_by_years_range(
                    self.year_start, self.year_end, self.limit, self.offset
                )
            else:
                movies = []

            if self.offset == 0:
                log_params: Dict[str, Any] = {}
                if self.search_mode in ("keyword", "genre", "year_single"):
                    log_params = {self.search_mode: self.user_current_query}
                elif self.search_mode == "year_range":
                    log_params = {"year_start": self.year_start, "year_end": self.year_end}

                count: int = len(movies) if movies else 0
                self._log_to_mongo(self.search_mode, log_params, count)

            current_page: int = (self.offset // self.limit) + 1

            if not movies:
                print("\nNo movies found matching your request.")
                self.reset_search_state()
                break

            self.show_results_visual(movies, current_page)

            print("\n" + "-" * 20)
            print("Page Management:")
            available_actions: Dict[str, str] = {}

            if len(movies) == self.limit:
                print("1. Next Page (Forward)")
                available_actions["1"] = "next"

            if self.offset > 0:
                print("2. Previous Page (Backward)")
                available_actions["2"] = "prev"

            print("0. Return to Main Menu")
            print("-" * 20)

            user_choice: str = input("Select an option: ").strip()

            if user_choice == "0":
                self.reset_search_state()
                break

            action: Optional[str] = available_actions.get(user_choice)

            if action == "next":
                self.offset += self.limit
            elif action == "prev":
                self.offset -= self.limit
            else:
                print("\n[!] Option unavailable or invalid key pressed! Please try again.")
                input("\nPress Enter to continue...")


    def reset_search_state(self) -> None:
        """
        Resets all variables relating to pagination limits, active filters, and search tracking parameters.
        """
        self.user_current_query = ""
        self.search_mode = ""
        self.offset = 0
        self.year_start = None
        self.year_end = None

    def _log_to_mongo(self, search_type: str, params: Dict[str, Any], results_count: int) -> None:
        """
        Constructs a structured search log and inserts it into MongoDB.
        """
        from datetime import datetime

        log_document: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }

        try:
            self.mongo.insert_log_into_mongo_db(log_document)
        except Exception as e:
            print(f"\n[Warning] Failed to save logs to MongoDB: {e}")
            input("Press Enter to continue...")

    def get_top_5_frequent(self) -> list:
        """
        Retrieves the top 5 most frequent search keywords from logs.
        """
        pipeline = [
            {"$match": {"search_type": "keyword", "params.keyword": {"$exists": True, "$ne": ""}}},
            {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        return list(self.mongo.aggregate(pipeline))

    def get_top_5_recent(self) -> list:
        """
        Retrieves the top 5 most recent queries from logs.
        """
        return list(self.mongo.find().sort("timestamp", -1).limit(5))

    def show_statistics_menu(self) -> None:
        """
        Displays the search analytics sub-menu and renders Top 5 statistics from MongoDB.
        """
        while True:
            self.clear_screen()
            print("╔" + "═" * 50 + "╗")
            print(f"║{'SEARCH STATISTICS (MONGODB)'.center(50)}║")
            print("╚" + "═" * 50 + "╝")
            print("\n  1. 📈 Top 5 Most Frequent Queries")
            print("  2. 🕒 Top 5 Most Recent Searches")
            print("  0. Back to Main Menu")
            print("-" * 52)

            choice: str = input("Select an option: ").strip()

            if choice == "0":
                break

            elif choice == "1":
                self.clear_screen()
                print("=== TOP 5 MOST FREQUENT QUERIES ===")
                data = self.mongo.get_top_5_frequent()

                if not data:
                    print("\nNo statistics available yet.")
                else:
                    for num, item in enumerate(data, 1):
                        print(f"  [{num}] Query: '{item['_id']}' — Searched {item['count']} times")

                input("\nPress Enter to go back...")


            elif choice == "2":

                self.clear_screen()

                print("=== TOP 5 MOST RECENT SEARCHES ===")

                data = self.mongo.get_top_5_recent()

                if not data:

                    print("\nNo statistics available yet.")

                else:
                    for num, item in enumerate(data, 1):
                        search_type: str = item.get('search_type', 'unknown')
                        params: dict = item.get('params', {})
                        raw_timestamp: str = item.get('timestamp', 'N/A')
                        clean_timestamp: str = raw_timestamp.replace('T', ' ').split('.')[0]
                        param_str = ", ".join([f"{k}: {v}" for k, v in params.items()])
                        print(f"  [{num}] [{clean_timestamp}] Mode: {search_type} | ({param_str})")
                input("\nPress Enter to go back...")