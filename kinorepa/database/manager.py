import sqlite3


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
            CREATE TABLE IF NOT EXISTS user (
                id                  UUID PRIMARY KEY,
            
                login               VARCHAR NOT NULL,
                name                VARCHAR NOT NULL,
                email               VARCHAR NOT NULL,
                
                is_online           BOOLEAN,
            
                registered_at       TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS user_login_idx ON
                user(login);
            
            CREATE TABLE IF NOT EXISTS film (
                id                  UUID PRIMARY KEY,
            
                filmcrew_id         UUID NOT NULL,
                genre               VARCHAR NOT NULL,

                kinopoisk_id        INTEGER NUT NULL,
                imdb_id             INTEGER NUT NULL,

                name_ru             VARCHAR NOT NULL,
                name_orig           VARCHAR NOT NULL,
                description         VARCHAR NOT NULL,

                budget              MONEY NOT NULL,
                fees                MONEY NOT NULL,
            
                duration            INTEGER NOT NULL,
            
                rating_kinopoisk    DECIMAL(5, 1) NOT NULL,
                rating_imdb         DECIMAL(5, 1) NOT NULL,
                rating_kinorepa     DECIMAL(5, 1) NOT NULL,
            
                release_year        TIMESTAMPTZ NOT NULL,
                updated_at          TIMESTAMPTZ NOT NULL,
                published_at        TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS  film_filmcrew_idx ON 
                film(filmcrew_id);
            
            CREATE INDEX IF NOT EXISTS  film_name_ru_idx ON
                film(name_ru);
            CREATE INDEX IF NOT EXISTS  film_name_orig_idx ON
                film(name_orig);
            
            CREATE INDEX IF NOT EXISTS  film_released_at_idx ON
                film(release_year);
            
            CREATE TABLE IF NOT EXISTS filmcrew (
                id                  UUID PRIMARY KEY,
            
                producer            VARCHAR NOT NULL,
                director            VARCHAR NOT NULL,
                screenwriter        VARCHAR NOT NULL,
                operator            VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS review_status (
                id                  UUID PRIMARY KEY,
            
                status_name         VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS review_type (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS review (
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
                review(user_id);
            
            CREATE TABLE IF NOT EXISTS wishlist_type (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS wishlist (
                id                  UUID PRIMARY KEY,
            
                user_id            	UUID NOT NULL,
                film_id             UUID NOT NULL,
                type_id             UUID NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS wishlist_user_id_idx ON
                wishlist(user_id);
            
            CREATE TABLE IF NOT EXISTS actor (
                id                  UUID PRIMARY KEY,
            
                first_name          VARCHAR NOT NULL,
                second_name         VARCHAR NOT NULL
            )
        """
        )

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
