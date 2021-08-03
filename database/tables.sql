CREATE TABLE principal (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    main_page JSONB NOT NULL
);

CREATE TABLE news (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    category TEXT NOT NULL,
    news JSONB NOT NULL
);

CREATE TABLE category (
    _id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    code INTEGER NOT NULL,
    is_enable BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE users (
    _id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "disabled" BOOLEAN NOT NULL DEFAULT FALSE,
    full_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE article (
    _id SERIAL PRIMARY KEY,
    "url" TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    article JSONB NOT NULL
);

CREATE TABLE front_page (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    "page" JSONB NOT NULL
);