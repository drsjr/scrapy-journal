--Get news by category with pagination

SELECT 
    c._id,
    c.created_at,
    c.news
FROM category c
WHERE c.category = 'ultimas'
GROUP BY c._id, c.news->'url_path' 
ORDER BY c._id DESC
OFFSET 0 FETCH NEXT 5 ROW ONLY