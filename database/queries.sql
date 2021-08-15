--Get news by category with pagination

SELECT 
    c._id,
    c.created_at,
    c.news
FROM category c
WHERE c.category = 'ultimas'
GROUP BY c._id, c.news->'url_path' 
ORDER BY c._id DESC
OFFSET 0 FETCH NEXT 5 ROW ONLY;

-- Get all Categories

SELECT 
    _id,
    "name",
    path,
    code
FROM category WHERE
is_enable = true;

SELECT 
    n.news->>'url_path',
    n.news->>'news_time',
    n.news->>'url_image',
    n.news->>'news_title',
    n.news->>'news_subtitle',
    category,
    created_at
FROM news n
WHERE n.news->>'url_path' = '/ultimas/2021/07/128236-policia-federal-combate-em-3-estados-venda-maconha-pela-internet.html'
GROUP BY n.news->>'url_path'

SELECT 
    n.article->>'url',
    n.article->>'time',
    n.article->>'title',
    n.article->>'subtitle',
    n.article->>'url_image',
    n.article->'paragraphs',
    category,
    created_at
FROM article n
WHERE n.article->>'url' = '/ultimas/2021/07/128236-policia-federal-combate-em-3-estados-venda-maconha-pela-internet.html'

