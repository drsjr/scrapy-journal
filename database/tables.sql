CREATE TABLE principal (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    main_page JSONB NOT NULL
);

CREATE TABLE category (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    category TEXT NOT NULL,
    news JSONB NOT NULLb
);

CREATE TABLE users (
    _id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "disabled" BOOLEAN NOT NULL DEFAULT FALSE,
    ful_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);