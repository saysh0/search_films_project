# Console Film Search Project 🎬

[English](#english) | [Русский](#русский)

---

## English

**Console Film Search Project** is a lightweight, Python-based CLI application designed for searching movies right from your terminal using the Kinopoisk API. It allows users to query film data, interact with a local database, and manage configurations seamlessly through a user-friendly console menu.

### ✨ Application Menu & Features
* **1. Search by Film Name** — Search for movies, TV shows, and cartoons using keywords or full titles via API.
* **2. Search by Film Category** — Search for movies, TV shows, and cartoons by selecting a category via API.
* **3. Search by Film Year/Period** — Search for movies, TV shows, and cartoons by a specific year or time period via API.
* **4. View Top 5 Most Popular/Recent Queries** — Displays the top 5 popular or recent search queries saved in MongoDB.
* **5. Exit** — Safely close the application and terminate all active connections, +easter egg.


### 📁 Project Structure
* `main.py` — The main entry point to start the application.
* `ui.py` — UI module handling the console interface, user inputs, and menus.
* `code.py` — Core logic for processing search queries and handling data.
* `config.py` — Configuration file for API keys, paths, and environment settings.
* `db/` — Directory containing the local database storage.
* `requirements.txt` — List of required external Python packages.

### 🚀 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/saysh0/search_films_project.git
   cd 'your path to the folder'/search_films_project
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   * Open `config.py` and insert your personal Kinopoisk API key.

4. **Run the Application:**
   ```bash
   python main.py
   ```

---

## Русский

**Console Film Search Project** — это легковесное консольное приложение на Python для быстрого поиска фильмов через API Кинопоиска. Программа позволяет искать информацию о кинокартинах, взаимодействовать с локальной базой данных и управлять настройками через интерактивное текстовое меню.

### ✨ Меню приложения и возможности
* **1. Поиск по названию фильма** — Поиск фильмов, сериалов и мультфильмов по ключевым словам или полному названию через API.
* **2. Поиск по категории фильма** — Поиск фильмов, сериалов и мультфильмов по выбору категории через API.
* **3. Поиск по году/периоду фильма** — Поиск фильмов, сериалов и мультфильмов по определенному году или периоду через API.
* **4. Просмотр топ-5 самых популярных запросов/последних запросов** — Отображает топ-5 популярных запросов/последних запросов, сохраненных в MongoDB.
* **5. Выход** — Безопасное закрытие приложения и завершение всех активных соединений, +пасхалка.

### 📁 Структура проекта
* `main.py` — Главная точка входа для запуска приложения.
* `ui.py` — Модуль, отвечающий за консольный интерфейс (меню, ввод/вывод данных).
* `code.py` — Основная логика поиска, запросов к API и обработки данных.
* `config.py` — Конфигурационный файл (настройки API, пути к локальным файлам).
* `db/` — Директория для хранения локальной базы данных SQLite.
* `requirements.txt` — Список внешних зависимостей проекта.

### 🚀 Инструкция по установке и запуску

1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/saysh0/search_films_project.git
   cd 'ваш путь к папке'/search_films_project
   ```

2. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка API ключа:**
   * Откройте файл `config.py` и добавьте ваш уникальный API-ключ Кинопоиска.

4. **Запуск приложения:**
   ```bash
   python main.py
   ```