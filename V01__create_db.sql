CREATE SCHEMA kinorepa;

CREATE TYPE kinorepa.user_status_t as ENUM (
    'offline',
    'online'
);

CREATE TABLE kinorepa.user (
    id                  TEXT PRIMARY KEY,

    login               TEXT NOT NULL,
    name                TEXT NOT NULL,
    email               TEXT NOT NULL,
    
    status              kinorepa.user_status_t NOT NULL,

    registered_at       TIMESTAMPTZ NOT NULL,
    last_online_at      TIMESTAMPTZ NOT NULL
);

CREATE INDEX user_login_idx ON 
    kinorepa.user(login);

CREATE TYPE kinorepa.film_genre_t as ENUM (
    'action',
    'comedy',
    'drama',
    'fantasy',
    'horror',
    'mystery',
    'romance',
    'thriller'
);

CREATE TABLE kinorepa.film (
    id                  TEXT PRIMARY KEY,
    filmcrew_id         TEXT NOT NULL,

    name                TEXT NOT NULL,
    fees                INTEGER NOT NULL,
    budget              INTEGER NOT NULL,

    genre               kinorepa.film_genre_t NOT NULL,
    duration            INTEGER NOT NULL,

    rating_kp           DECIMAL(5, 1) NOT NULL,
    rating_imdb         DECIMAL(5, 1) NOT NULL,
    rating              DECIMAL(5, 1) NOT NULL,

    published_at        TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL
);

CREATE INDEX film_filmcrew_idx ON 
    kinorepa.film(filmcrew_id);

CREATE INDEX film_name_idx ON
    kinorepa.film(name);

CREATE TABLE kinorepa.filmcrew (
    id                  TEXT PRIMARY KEY,

    producer            TEXT NOT NULL,
    director            TEXT NOT NULL,
    screenwriter        TEXT NOT NULL,
    operator            TEXT NOT NULL
);

CREATE TYPE kinorepa.review_status_t as ENUM (
    'draft',
    'published',
    'hidden',
    'deleted'
);

CREATE TYPE kinorepa.review_type_t as ENUM (
    'positive',
    'negative'
);

CREATE TABLE kinorepa.review (
    id                  TEXT PRIMARY KEY,

    user_id             TEXT NOT NULL,
    film_id             TEXT NOT NULL,

    score               DECIMAL(5,1) NOT NULL,

    type                kinorepa.review_type_t NOT NULL,
    status              kinorepa.review_status_t NOT NULL,

    text                TEXT NOT NULL

    created_at          TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL
);

CREATE INDEX review_user_id_idx ON
    kinorepa.review(user_id);
