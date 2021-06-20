CREATE TABLE principal (
    _id SERIAL PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    main_page JSONB NOT NULL
);