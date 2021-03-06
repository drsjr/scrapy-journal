CREATE TABLE article (
    _id SERIAL PRIMARY KEY,
    "url" TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    article JSONB NOT NULL
);

CREATE TABLE category_news (
    _id SERIAL PRIMARY KEY,
    "url" TEXT NOT NULL,
    category TEXT NOT NULL,
    category_code INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE front_page (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    "page" JSONB NOT NULL
);

CREATE TABLE news (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    "url" TEXT NOT NULL
);


DELETE FROM article;
DELETE FROM category_news;
DELETE FROM front_page;
DELETE FROM news;
