import etl_scrapy_database as etl
import manage
import time




#
# python3 -c 'import worker; worker.reload_news()'
#
def reload_news():
    scrapy_finished = False
    print("start::reload_news_info, ", scrapy_finished)
    manage.all_calls()

    while scrapy_finished is False:
        all_jobs = manage.list_jobs()
        scrapy_finished = (len(all_jobs["running"]) == 0 and len(all_jobs["pending"]) == 0)
        time.sleep(5)

    print("ended::reload_news_info, ", scrapy_finished)

    etl.all_calls()


def thread_process():
    l = True

    while l is True:
        reload_news()
        #Send Message
        time.sleep(600)