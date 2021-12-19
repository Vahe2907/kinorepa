import psycopg2

class DBManager:
    dbname = None
    user = None
    password = None
    host = 'localhost'
    cursor = None
    conn = None

    def __init__(self, dbname, user, password):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        self.cursor = self.conn.cursor()
        self.init_tables()
        self.conn.commit()

    def init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS kinorepa.user (
                id                  UUID PRIMARY KEY,
            
                login               VARCHAR NOT NULL,
                name                VARCHAR NOT NULL,
                email               VARCHAR NOT NULL,
                
                is_online           BOOLEAN,
            
                registered_at       TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS user_login_idx ON
                kinorepa.user(login);
            
            CREATE TABLE IF NOT EXISTS kinorepa.film_genre (
                id                  UUID PRIMARY KEY,
            
                genre_name          VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS kinorepa.film (
                id                  UUID PRIMARY KEY,
            
                filmcrew_id         UUID NOT NULL,
                genre_id            UUID NOT NULL,

                name                VARCHAR NOT NULL,
                fees                MONEY NOT NULL,
                budget              MONEY NOT NULL,
            
                duration            INTEGER NOT NULL,
            
                rating_kp           DECIMAL(5, 1) NOT NULL,
                rating_imdb         DECIMAL(5, 1) NOT NULL,
                rating              DECIMAL(5, 1) NOT NULL,
            
                released_at         TIMESTAMPTZ NOT NULL,
                published_at        TIMESTAMPTZ NOT NULL,
                updated_at          TIMESTAMPTZ NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS  film_filmcrew_idx ON 
                kinorepa.film(filmcrew_id);
            
            CREATE INDEX IF NOT EXISTS  film_name_idx ON
                kinorepa.film(name);
            
            CREATE INDEX IF NOT EXISTS  film_released_at_idx ON
                kinorepa.film(released_at);
            
            CREATE TABLE IF NOT EXISTS kinorepa.filmcrew (
                id                  UUID PRIMARY KEY,
            
                producer            VARCHAR NOT NULL,
                director            VARCHAR NOT NULL,
                screenwriter        VARCHAR NOT NULL,
                operator            VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS kinorepa.review_status (
                id                  UUID PRIMARY KEY,
            
                status_name         VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS kinorepa.review_type (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS kinorepa.review (
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
                kinorepa.review(user_id);
            
            CREATE TABLE IF NOT EXISTS kinorepa.wishlist_type (
                id                  UUID PRIMARY KEY,
            
                type_name           VARCHAR NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS kinorepa.wishlist (
                id                  UUID PRIMARY KEY,
            
                user_id            	UUID NOT NULL,
                film_id             UUID NOT NULL,
                type_id             UUID NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS wishlist_user_id_idx ON
                kinorepa.wishlist(user_id);
            
            CREATE TABLE IF NOT EXISTS kinorepa.actor (
                id                  UUID PRIMARY KEY,
            
                first_name          VARCHAR NOT NULL,
                second_name         VARCHAR NOT NULL
            )
        """)

    def find_by_filters(self, genres, duration_min, duration_max, name, year):
        self.cursor.execute(f"""SELECT * FROM kinorepa.film
        WHERE film.genre_id IN (
            SELECT id FROM kinorepa.film_genre
            WHERE ({genres} IS NULL OR film_genre.genre_name IN ({genres}))
        )
        AND ({duration_min} IS NULL OR film.duration >= {duration_min})
        AND ({duration_max} IS NULL OR film.duration <= {duration_max})
        AND ({name} IS NULL OR film.name LIKE '%{name}%')
        AND ({year} IS NULL OR  film.published_at > make_timestamptz({year}, 01, 01, 0, 0, 1))""")
        return self.cursor.fetchone()
