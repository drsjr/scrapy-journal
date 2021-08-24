SELECT 
    nl.id,
    nc.id,
    nm.id,
    ar.id
FROM front_page fp
INNER JOIN news_column nl ON 
    nl.front_page_id = fp.id
INNER JOIN news_carrossel nc ON 
    nc.front_page_id = fp.id
INNER JOIN news_main nm ON 
    nm.front_page_id = fp.id
INNER JOIN article ar ON 
    nc.article_id = ar.id OR
    nl.article_id = ar.id OR
    nm.article_id = ar.id;

SELECT * FROM news_main, news_column, news_carrossel

SELECT * FROM article;

SELECT 
    t.is_from,
    t.id,
    t.url,
    t.title,
    t.subtitle,
    t.image,
    t.category_id,
    t.created_at,
    t.front_page_id
FROM (
    SELECT
        'main' AS is_from,
        ar.id,
        ar.url,
        ar.title,
        ar.subtitle,
        ar.image,
        ar.category_id,
        ar.created_at,
        fp.id AS front_page_id
    FROM front_page fp
    INNER JOIN news_main n ON n.front_page_id = fp.id
    INNER JOIN article ar ON n.article_id = ar.id
    UNION
    SELECT 
        'carrossel' AS is_from,
        ar.id,
        ar.url,
        ar.title,
        ar.subtitle,
        ar.image,
        ar.category_id,
        ar.created_at,
        fp.id AS front_page_id
    FROM front_page fp
    INNER JOIN news_carrossel n ON n.front_page_id = fp.id
    INNER JOIN article ar ON n.article_id = ar.id
    UNION
    SELECT 
        'column' AS is_from,
        ar.id,
        ar.url,
        ar.title,
        ar.subtitle,
        ar.image,
        ar.category_id,
        ar.created_at,
        fp.id AS front_page_id
    FROM front_page fp
    INNER JOIN news_column n ON n.front_page_id = fp.id
    INNER JOIN article ar ON n.article_id = ar.id) AS t
WHERE t.front_page_id = 9;



