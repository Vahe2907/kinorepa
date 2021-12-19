CREATE SCHEMA kinorepa;

CREATE TABLE kinorepa.user (
    id                  UUID PRIMARY KEY,

    login               VARCHAR NOT NULL,
    name                VARCHAR NOT NULL,
    email               VARCHAR NOT NULL,
    
    is_online           BOOLEAN,

    registered_at       TIMESTAMPTZ NOT NULL
);

CREATE INDEX user_login_idx ON
    kinorepa.user(login);

CREATE TABLE kinorepa.film_genre (
    id                  UUID PRIMARY KEY,

    genre_name          VARCHAR NOT NULL
);

CREATE TABLE kinorepa.film (
    id                  UUID PRIMARY KEY,

    filmcrew_id         UUID NOT NULL,
    genre_id            UUID NOT NULL,
    actor_id            UUID NOT NULL,

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

CREATE INDEX film_filmcrew_idx ON 
    kinorepa.film(filmcrew_id);

CREATE INDEX film_name_idx ON
    kinorepa.film(name);

CREATE INDEX film_released_at_idx ON
    kinorepa.film(released_at);

CREATE TABLE kinorepa.filmcrew (
    id                  UUID PRIMARY KEY,

    producer            VARCHAR NOT NULL,
    director            VARCHAR NOT NULL,
    screenwriter        VARCHAR NOT NULL,
    operator            VARCHAR NOT NULL
);

CREATE TABLE kinorepa.review_status (
    id                  UUID PRIMARY KEY,

    status_name         VARCHAR NOT NULL
);

CREATE TABLE kinorepa.review_type (
    id                  UUID PRIMARY KEY,

    type_name           VARCHAR NOT NULL
);

CREATE TABLE kinorepa.review (
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

CREATE INDEX review_user_id_idx ON
    kinorepa.review(user_id);

CREATE TABLE kinorepa.wishlist_type (
    id                  UUID PRIMARY KEY,

    type_name           VARCHAR NOT NULL
);

CREATE TABLE kinorepa.wishlist (
    id                  UUID PRIMARY KEY,

    user_id            	UUID NOT NULL,
    film_id             UUID NOT NULL,
    type_id             UUID NOT NULL
);

CREATE INDEX wishlist_user_id_idx ON
    kinorepa.wishlist(user_id);

CREATE TABLE kinorepa.actor (
    id                  UUID PRIMARY KEY,

    first_name          VARCHAR NOT NULL,
    second_name         VARCHAR NOT NULL
)
