
import os
from typing import List
from model import News, User
import psycopg2

class Database():

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.connection = psycopg2.connect(
            host='192.168.15.35',
            user='folha',
            password='folha',
            dbname='folha',
            port=5432)


class UserRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()
    
    def get_query_by_username(self, username: str) -> User:
        self.cursor.execute("SELECT username, password, full_name, disabled FROM users where username = %s", [username])
        obj = self.cursor.fetchone()
        if obj is None:
            return None
        user = User(username=obj[0], password=obj[1], full_name=obj[2], disabled=False)
        return user


class NewsRepository():

    def __init__(self, db: Database) -> List[News]:
        self.cursor = db.connection.cursor()


    def get_query_category_pagination(self, category: str, offset: int = 0, limit: int = 5):
        response = []
        query = """
            SELECT 
                c._id,
                c.created_at,
                c.news
            FROM category c
            WHERE c.category = %s
            GROUP BY c._id, c.news->'url_path' 
            ORDER BY c._id DESC
            OFFSET %s FETCH NEXT %s ROW ONLY
        """
        self.cursor.execute(query, [category, offset, limit])
        result = self.cursor.fetchall()
        for obj in result:
            response.append(
                News(id=obj[0], 
                    url_path=obj[2]["url_path"], 
                    url_image=obj[2]["url_image"], 
                    title=obj[2]["news_title"], 
                    subtitle=obj[2]["news_subtitle"], 
                    time=obj[2]["news_time"], 
                    category=category)
                )

        return response



