import psycopg2

POSTGRES_HOSTNAME = "172.17.0.2"
POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_DBNAME = "journal_jj"

QUERY_VERIFY_ARTICLE_BY_URL = "SELECT url FROM article WHERE url = %s;"

QUERY_VERIFY_NEWS_MAIN = "SELECT id FROM news_main WHERE front_page_id = %s AND article_id = %s"

QUERY_VERIFY_NEWS_COLUMN = "SELECT id FROM news_column WHERE front_page_id = %s AND article_id = %s"

QUERY_VERIFY_NEWS_CARROSSEL = "SELECT id FROM news_carrossel WHERE front_page_id = %s AND article_id = %s"

QUERY_GET_LAST_FRONT_PAGE_ID = "SELECT id FROM front_page ORDER BY id DESC LIMIT 1;"


QUERY_GET_ALL_NEWS_URL = "SELECT url FROM article;"

QUERY_GET_ARTICLE_BY_URL = "SELECT * FROM article WHERE url = %s;"

QUERY_GET_CATEGORY_BY_NAME = "SELECT id FROM category WHERE name = %s;"

INSERT_INTO_ARTICLE = """
    INSERT INTO article (url, title, subtitle, image, created_at, category_id)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

INSERT_INTO_PARAGRAPH = """
    INSERT INTO paragraph (article_id, \"order\", paragraph)
    VALUES (%s, %s, %s)
"""

INSERT_INTO_FRONT_PAGE = """
    INSERT INTO front_page (created_at) VALUES (%s);
"""

INSERT_INTO_NEWS_MAIN = """
    INSERT INTO news_main (front_page_id, article_id) VALUES (%s, %s);
"""

INSERT_INTO_NEWS_COLUMN = """
    INSERT INTO news_column (front_page_id, article_id) VALUES (%s, %s);
"""

INSERT_INTO_NEWS_CARROSSEL = """
    INSERT INTO news_carrossel (front_page_id, article_id) VALUES (%s, %s);
"""

SELECT_ARTICLE_BY_URL = """
    SELECT id FROM article WHERE url = %s;
"""

class ProdDatabase():

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.connection = psycopg2.connect(

            host=POSTGRES_HOSTNAME, 
            user=POSTGRES_USERNAME, 
            password=POSTGRES_PASSWORD, 
            dbname=POSTGRES_DBNAME,
            port=POSTGRES_PORT)
        
        self.cursor = None

    def get_cursor(self):
        if self.cursor is None:
            self.cursor = self.connection.cursor()
        return self.cursor

    def close_cursor(self):
        if self.cursor is not None:
            self.cursor.close()

    def get_category_by_name(self, name: str) -> int:
        self.get_cursor().execute(QUERY_GET_CATEGORY_BY_NAME, [name])
        id = self.get_cursor().fetchone()
        return id


    def get_front_page_id(self) -> int:
        self.get_cursor().execute(QUERY_GET_LAST_FRONT_PAGE_ID, [])
        id = self.get_cursor().fetchone()[0]
        return id


    def get_article_by_url(self, url: str):
        self.get_cursor().execute(QUERY_GET_ARTICLE_BY_URL, [url])
        article = self.get_cursor().fetchone()
        return article


    def i_o():
        pass

##### VERIFY

    def verify_article(self, url: str) -> bool:
        self.get_cursor().execute(QUERY_VERIFY_ARTICLE_BY_URL, [url])
        value = self.get_cursor().fetchone()
        return (value is None)

    def verify_news_main(self, front_page_id: int, article_id: int) -> bool:
        self.get_cursor().execute(QUERY_VERIFY_NEWS_MAIN, [front_page_id, article_id])
        value = self.get_cursor().fetchone()
        return (value is None)

    def verify_news_column(self, front_page_id: int, article_id: int) -> bool:
        self.get_cursor().execute(QUERY_VERIFY_NEWS_COLUMN, [front_page_id, article_id])
        value = self.get_cursor().fetchone()
        return (value is None)

    def verify_news_carrossel(self, front_page_id: int, article_id: int) -> bool:
        self.get_cursor().execute(QUERY_VERIFY_NEWS_CARROSSEL, [front_page_id, article_id])
        value = self.get_cursor().fetchone()
        return (value is None)

##### INSERTS

    def insert_article(self, url: str, title: str, subtitle: str, image: str, created_at: str, category_id: int):
        self.get_cursor().execute(INSERT_INTO_ARTICLE, [url, title, subtitle, image, created_at, category_id])
        
    def insert_paragraph(self, article_id: int, order: int, paragraph: str):
        self.get_cursor().execute(INSERT_INTO_PARAGRAPH, [article_id, order, paragraph])

    def insert_front_page(self, created_at: str):
        self.get_cursor().execute(INSERT_INTO_FRONT_PAGE, [created_at])

    def insert_main_news(self, front_page_id: int, article_id: int):
        self.get_cursor().execute(INSERT_INTO_NEWS_MAIN, [front_page_id, article_id])

    def insert_news_column(self, front_page_id: int, article_id: int):
        self.get_cursor().execute(INSERT_INTO_NEWS_COLUMN, [front_page_id, article_id])

    def insert_news_carrossel(self, front_page_id: int, article_id: int):
        self.get_cursor().execute(INSERT_INTO_NEWS_CARROSSEL, [front_page_id, article_id])
        
