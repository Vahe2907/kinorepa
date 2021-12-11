CREATE SCHEMA kinorepa;

CREATE TYPE kinorepa.user_status_t as ENUM (
    'offline',
    'online'
);

CREATE TABLE kinorepa.user (
    id                  GUID PRIMARY KEY,

    login               VARCHAR(MAX) NOT NULL,
    name                VARCHAR(MAX) NOT NULL,
    email               VARCHAR(MAX) NOT NULL,
    
    status              kinorepa.user_status_t NOT NULL,

    registered_at       TIMESTAMPTZ NOT NULL,
    last_online_at      TIMESTAMPTZ NOT NULL
);

CREATE INDEX user_login_idx ON 
    kinorepa.user(login);

CREATE TYPE kinorepa.film_genre (
    id                  GUID PRIMARY KEY,

    genre_name          VARCHAR(MAX) NOT NULL
);

CREATE TABLE kinorepa.film (
    id                  GUID PRIMARY KEY,

    filmcrew_id         GUID NOT NULL,
    genre_id            GUID NOT NULL,

    name                VARCHAR(MAX) NOT NULL,
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

CREATE INDEX film_filmcrew_idx ON 
    kinorepa.film(filmcrew_id);

CREATE INDEX film_name_idx ON
    kinorepa.film(name);

CREATE INDEX film_released_at_idx ON
    kinorepa.film(released_at);

CREATE TABLE kinorepa.filmcrew (
    id                  GUID PRIMARY KEY,

    producer            VARCHAR(MAX) NOT NULL,
    director            VARCHAR(MAX) NOT NULL,
    screenwriter        VARCHAR(MAX) NOT NULL,
    operator            VARCHAR(MAX) NOT NULL
);

CREATE TABLE kinorepa.review_status (
    id                  GUID PRIMARY KEY,

    status_name         VARCHAR(MAX) NOT NULL
);

CREATE TYPE kinorepa.review_type (
    id                  GUID PRIMARY KEY,

    type_name           VARCHAR(MAX) NOT NULL
);

CREATE TABLE kinorepa.review (
    id                  GUID PRIMARY KEY,

    user_id             GUID NOT NULL,
    film_id             GUID NOT NULL,
    review_status_id    GUID NOT NULL,
    review_type_id      GUID NOT NULL,

    score               DECIMAL(5,1) NOT NULL,

    text                VARCHAR(MAX) NOT NULL

    created_at          TIMESTAMPTZ NOT NULL,
    updated_at          TIMESTAMPTZ NOT NULL
);

CREATE INDEX review_user_id_idx ON
    kinorepa.review(user_id);

CREATE TYPE kinorepa.wishlist_type (
    id                  GUID PRIMARY KEY,

    type_name           VARCHAR(MAX) NOT NULL
);

CREATE TABLE kinorepa.wishlist (
    id                  GUID PRIMARY KEY,

    user_id            	GUID NOT NULL,
    film_id             GUID NOT NULL,
    type_id             GUID NOT NULL
);

CREATE INDEX wishlist_user_id_idx ON
    kinorepa.wishlist(user_id);
