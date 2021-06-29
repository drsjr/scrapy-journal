import os


category_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=categories -d category={0}'
category_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0}'

principal_spider_api_call = 'curl http://192.168.15.35:6800/schedule.json -d project=journal -d spider=principal'
principal_spider_api_call_local = 'curl http://localhost:6800/schedule.json -d project=journal -d spider=principal'

categories = [ 'ultimas', 'jundiai', 'opiniao', 'politica', 'economia', 'policia', 'esportes', 'cultura', 'hype']


def call_all_categories():
    for c in categories:
        os.system(category_spider_api_call_local.format(c))

def call_principal():
    os.system(principal_spider_api_call_local)
