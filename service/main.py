import os
import json
from datetime import datetime
from typing import Dict
from fastapi import FastAPI

# From

app = FastAPI()


list_news = json.loads(open("list_news.json", "r").read())
list_articles = json.loads(open("list_article.json", "r").read())


@app.get("/news/{news_id}")
def article(news_id: int):
    return get_article_by_id(news_id)


@app.get("/news")
def news() -> []:
    return get_list_news()

def get_list_news():
    return list_news

def get_article_by_id(id: int):
    return list_articles[id]