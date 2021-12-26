# adding kinorepa directory
import sys

sys.path.append("../../kinorepa")

import sqlite3
import typing

from kinorepa.models import film, fact


class DBManager:
    """
    Утилита для работы с базами данных с помощью библиотеки sqlite3
    """

    def __init__(self, db_name: str):
        self.db_name: str = db_name

        self.connection: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

        self.init_tables()
        self.connection.commit()

    def init_tables(self):
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id                  UUID PRIMARY KEY,
            
                login               VARCHAR NOT NULL,
                name                VARCHAR NOT NULL,
            
                registered_at       TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS user_login_idx ON
                users(login);
            
            CREATE TABLE IF NOT EXISTS films (
                id                  UUID PRIMARY KEY,
            
                filmcrew_id         UUID,
                genres               VARCHAR,

                kinopoisk_id        INTEGER NUT NULL,
                imdb_id             INTEGER,

                name_ru             VARCHAR,
                name_orig           VARCHAR,
                description         VARCHAR,

                budget              MONEY,
                fees                MONEY,
            
                duration            INTEGER,
            
                rating_kinopoisk    DECIMAL(5, 1),
                rating_imdb         DECIMAL(5, 1),
                rating_kinorepa     DECIMAL(5, 1),
            
                release_year        TIMESTAMPTZ,
                updated_at          TIMESTAMPTZ NOT NULL,
                published_at        TIMESTAMPTZ,

                poster_url          VARCHAR
            );
            
            CREATE INDEX IF NOT EXISTS  film_filmcrew_idx ON 
                films(filmcrew_id);
            
            CREATE INDEX IF NOT EXISTS  film_name_ru_idx ON
                films(name_ru);
            CREATE INDEX IF NOT EXISTS  film_name_orig_idx ON
                films(name_orig);
            
            CREATE INDEX IF NOT EXISTS  film_released_at_idx ON
                films(release_year);
            
            CREATE TABLE IF NOT EXISTS filmcrews (
                id                  UUID PRIMARY KEY,
            
                producer            VARCHAR NOT NULL,
                director            VARCHAR NOT NULL,
                screenwriter        VARCHAR NOT NULL,
                operator            VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS review_statuses (
                id                  UUID PRIMARY KEY,
            
                status_name         VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS review_types (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS reviews (
                id                  UUID PRIMARY KEY,
            
                user_id             UUID NOT NULL,
                film_id             UUID NOT NULL,
                review_status_id    UUID NOT NULL,
                review_type_id      UUID NOT NULL,
            
                score               DECIMAL(5,1) NOT NULL,
            
                text                VARCHAR NOT NULL,
            
                created_at          TIMESTAMPTZ NOT NULL,
                updated_at          TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS review_user_id_idx ON
                reviews(user_id);
            
            CREATE TABLE IF NOT EXISTS wishlist_types (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS wishlists (
                id                  INTEGER PRIMARY KEY,

                user_id             UUID NOT NULL,

                film_id             UUID NOT NULL,
                type_id             UUID NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS wishlist_user_id_idx ON
                wishlists(user_id);
            
            CREATE TABLE IF NOT EXISTS actors (
                id                  UUID PRIMARY KEY,
            
                first_name          VARCHAR NOT NULL,
                second_name         VARCHAR NOT NULL
            );

            CREATE TABLE IF NOT EXISTS facts (
                id                  INTEGER PRIMARY KEY,
            
                film_id             UUID NOT NULL,
                
                text                VARCHAR NOT NULL,
                is_spoiler          INTEGER NOT NULL
            )
        """
        )

    def is_user_registered(self, user_id):
        try:
            self.cursor.execute(f"""SELECT id FROM users WHERE id = {user_id}""")
            user_in_db = self.cursor.fetchone()
            return user_in_db != None
        except sqlite3.Error as err:
            print("An error occurred: ", err.args[0])
            return False

    def register_user(self, user_id, login, name, registered_at):
        try:
            self.cursor.execute(
                f"""INSERT INTO users VALUES(?, ?, ?, ?)""",
                (user_id, login, name, registered_at),
            )
            self.cursor.fetchone()
        except sqlite3.Error as err:
            print("An error occurred: ", err.args[0])

    def find_by_filters(self, genres, duration_min, duration_max, name, year):
        self.cursor.execute(
            f"""SELECT * FROM film
        WHERE film.genre_id IN (
            SELECT id FROM film_genre
            WHERE ({genres} IS NULL OR film_genre.genre_name IN ({genres}))
        )
        AND ({duration_min} IS NULL OR film.duration >= {duration_min})
        AND ({duration_max} IS NULL OR film.duration <= {duration_max})
        AND ({name} IS NULL OR film.name LIKE '%{name}%')
        AND ({year} IS NULL OR  film.published_at > make_timestamptz({year}, 01, 01, 0, 0, 1))"""
        )
        return self.cursor.fetchone()

    def insert_film(self, film_to_insert: film.Film):
        try:
            self.cursor.execute(
                """
                INSERT INTO
                    films
                VALUES (
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?
                )
                """,
                film_to_insert.to_list,
            )
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def find_film_by_id(self, id: int) -> film.Film:
        try:
            self.cursor.execute(
                f"""
                SELECT * FROM
                    films
                WHERE
                    id = {id}
                """
            )
            found_film = self.cursor.fetchone()
            if found_film is not None:
                return film.parse_db(found_film)

            return None
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def insert_facts(self, facts: typing.List[fact.Fact]):
        try:
            self.cursor.executemany(
                """
                INSERT INTO facts (
                    film_id,

                    text,
                    is_spoiler
                ) VALUES (
                    ?, ?, ?
                )
                """,
                [item.to_list for item in facts],
            )
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def find_facts_ids_by_film_id(self, film_id: int) -> typing.List[fact.Fact]:
        try:
            self.cursor.execute(
                f"""
                SELECT
                    id
                FROM facts WHERE
                    film_id = {film_id}
                """
            )
            return [item[0] for item in self.cursor.fetchall()]
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def find_fact_by_id(self, id: int) -> fact.Fact:
        try:
            self.cursor.execute(
                f"""
                SELECT
                    film_id,

                    text,
                    is_spoiler
                FROM facts WHERE
                    id = {id}
                """
            )
            found_fact = self.cursor.fetchone()
            if found_fact is None:
                return None

            return fact.parse_db(found_fact)
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def add_to_wishlist(self, user_id, film_id, wishlist_type):
        try:
            self.cursor.execute(
                f"""
                INSERT INTO wishlists(user_id, film_id, type_id)
                VALUES(?, ?, ?)
                """,
                [user_id, film_id, wishlist_type],
            )
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])

    def add_liked_film(self, user_id, film_id):
        self.add_to_wishlist(user_id, film_id, 1)

    def add_to_watch_film(self, user_id, film_id):
        self.add_to_wishlist(user_id, film_id, 2)

    def get_liked_films(self, user_id):
        return self.get_film_ids_from_wishlist(user_id, 1)

    def get_to_watch_films(self, user_id):
        return self.get_film_ids_from_wishlist(user_id, 2)

    def get_film_ids_from_wishlist(self, user_id, wishlist_type):
        try:
            self.cursor.execute(
                f"""
                SELECT film_id FROM wishlists
                WHERE user_id = {user_id}
                AND type_id = {wishlist_type}
                """
            )
            return [item[0] for item in self.cursor.fetchall()]
        except sqlite3.Error as err:
            print("An error occurred:", err.args[0])
