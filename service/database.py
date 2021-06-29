from model import User
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



