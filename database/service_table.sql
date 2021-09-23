CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    "password" TEXT NOT NULL,
    full_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    "disabled" BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    code INT NOT NULL,
    "disabled" BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE article (
    id SERIAL PRIMARY KEY,
    "url" TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    title TEXT NOT NULL,
    subtitle TEXT NOT NULL,
    "image" TEXT NOT NULL,
    category_id INT NOT NULL,
    CONSTRAINT fk_category_article FOREIGN KEY(category_id) REFERENCES category(id)
);

CREATE TABLE paragraph (
    id SERIAL PRIMARY KEY,
    article_id INT NOT NULL,
    paragraph TEXT NOT NULL,
    "order" INT NOT NULL,
    CONSTRAINT fk_article_paragraph FOREIGN KEY(article_id) REFERENCES article(id)
);

CREATE TABLE front_page (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE news_other (
    id SERIAL PRIMARY KEY,
    front_page_id INT NOT NULL,
    article_id INT NOT NULL,
    CONSTRAINT fk_front_page_news_other FOREIGN KEY(front_page_id) REFERENCES front_page(id),
    CONSTRAINT fk_article_news_other FOREIGN KEY(article_id) REFERENCES article(id)
);

CREATE TABLE news_column (
    id SERIAL PRIMARY KEY,
    front_page_id INT NOT NULL,
    article_id INT NOT NULL,
    CONSTRAINT fk_front_page_news_column FOREIGN KEY(front_page_id) REFERENCES front_page(id),
    CONSTRAINT fk_article_news_column FOREIGN KEY(article_id) REFERENCES article(id)
);

CREATE TABLE news_carrossel (
    id SERIAL PRIMARY KEY,
    front_page_id INT NOT NULL,
    article_id INT NOT NULL,
    CONSTRAINT fk_front_page_news_carrossel FOREIGN KEY(front_page_id) REFERENCES front_page(id),
    CONSTRAINT fk_article_news_carrossel FOREIGN KEY(article_id) REFERENCES article(id)
);

CREATE TABLE news_main (
    id SERIAL PRIMARY KEY,
    front_page_id INT NOT NULL,
    article_id INT NOT NULL,
    CONSTRAINT fk_front_page_news_main FOREIGN KEY(front_page_id) REFERENCES front_page(id),
    CONSTRAINT fk_article_news_main FOREIGN KEY(article_id) REFERENCES article(id)
);


--DELETE Order


DELETE FROM news_main;
DELETE FROM news_carrossel;
DELETE FROM news_column;
DELETE FROM news_other;
DELETE FROM front_page;
DELETE FROM paragraph;
DELETE FROM article;
DELETE FROM category;
DELETE FROM user;
