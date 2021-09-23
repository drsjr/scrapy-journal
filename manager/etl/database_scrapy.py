import psycopg2


POSTGRES_HOSTNAME = "172.17.0.2"
POSTGRES_PORT = 5432
POSTGRES_USERNAME = "folha"
POSTGRES_PASSWORD = "folha"
POSTGRES_DBNAME = "folha"


QUERY_GET_FRONT_PAGE = "SELECT created_at, f.page FROM front_page f ORDER BY _id DESC LIMIT 1;"
QUERY_GET_ALL_NEWS_URL = "SELECT url FROM article;"
QUERY_GET_ARTICLE_BY_URL = "SELECT * FROM article WHERE url = %s;"
QUERY_VERIFY_ARTICLE_BY_URL = "SELECT url FROM article WHERE url = %s;"

class ScrapyDatabase():

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

    def get_all_news_url(self):
        self.get_cursor().execute(QUERY_GET_ALL_NEWS_URL, [])
        all_urls = self.get_cursor().fetchall()
        return all_urls

    def get_new_url_from_front_page(self):
        self.get_cursor().execute(QUERY_GET_FRONT_PAGE, [])
        f = self.get_cursor().fetchone()

        return { 
            "main": f[1]["main_news"]["url"], 
            "column": [i["url"] for i in f[1]["column_news"]], 
            "carrossel": [i["url"] for i in f[1]["carrossel"]], 
            "other": f[1]["other_news"], 
            "created_at": str(f[0]) 
            }
    
    #(1,
    #'/ultimas/2021/08/132128-zona-norte-registra-qualidade-pessima-do-ar-e-sao-paulo-nao-apresenta-regiao-com-indice-positivo.html',
    #datetime.datetime(2021, 8, 23, 19, 24),
    #'Zona norte registra qualidade péssima do ar e São Paulo não apresenta região com índice positivo',
    #'\r\nSegundo órgão, o índice ficou ruim após o incêndio do Parque Estadual Juquery',
    #'https://www.jj.com.br/_midias/jpg/2021/08/20/600x450/1__dsc6990-499341.jpg',
    #1)
    def get_article_by_url(self, url: str):
        self.get_cursor().execute(QUERY_GET_ARTICLE_BY_URL, [url])
        article = self.get_cursor().fetchone()
        return article



