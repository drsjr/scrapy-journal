import manage
import time

#
# python3 -c 'import worker; worker.thread_process()'
#

def thread_process():
    l = True

    while l is True:
        manage.call_crawling_front_page()
        print("sleep::nice")
        time.sleep(900)

