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