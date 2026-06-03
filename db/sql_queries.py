SEARCH_FILM_BY_TITLE = """SELECT f.title, f.description, f.release_year, f.length, group_concat(c.name SEPARATOR ', ') as film_categories
                         from film f
                         join film_category fc on f.film_id = fc.film_id
                         join category c on fc.category_id = c.category_id 
                         WHERE f.title LIKE %s
                         GROUP BY f.film_id
                         ORDER BY f.title DESC
                         LIMIT %s 
                         OFFSET %s"""


SHOW_ALL_CATEGORIES = """SELECT name 
                         FROM category"""


MINIMAL_YEAR_FOR_FILM = """SELECT min(release_year) as release_year
                           FROM film"""


MAXIMAL_YEAR_FOR_FILM = """SELECT max(release_year) as release_year
                           FROM film"""


SEARCH_FILM_BY_CATEGORY = """SELECT f.title, f.description, f.release_year, f.length, group_concat(c.name SEPARATOR ', ') as film_categories
                             from film f
                             join film_category fc on f.film_id = fc.film_id
                             join category c on fc.category_id = c.category_id 
                             WHERE c.name LIKE %s
                             GROUP BY f.film_id
                             ORDER BY f.title DESC
                             LIMIT %s 
                             OFFSET %s"""


SEARCH_FILM_BY_YEAR = """SELECT f.title, f.description, f.release_year, f.length, group_concat(c.name SEPARATOR ', ') as film_categories
                         from film f
                         join film_category fc on f.film_id = fc.film_id
                         join category c on fc.category_id = c.category_id 
                         WHERE f.release_year = %s
                         GROUP BY f.film_id
                         ORDER BY f.release_year DESC
                         LIMIT %s 
                         OFFSET %s"""


SEARCH_FILM_BY_YEAR_RANGE = """SELECT f.title, f.description, f.release_year, f.length, group_concat(c.name SEPARATOR ', ') as film_categories
                               from film f
                               join film_category fc on f.film_id = fc.film_id
                               join category c on fc.category_id = c.category_id 
                               WHERE f.release_year between %s and %s
                               GROUP BY f.film_id
                               ORDER BY f.release_year DESC
                               LIMIT %s 
                               OFFSET %s"""