import requests


URL = "http://localhost:6800/schedule.json"

SCHEDULE_RESOURCE = "http://localhost:6800/schedule.json"
LIST_JOB_RESOURCE = "http://localhost:6800/listjobs.json?project=journal"


def verify_all_jobs_finished() -> bool:
    jobs = get_all_schedule_job()
    return len(jobs["pending"]) == 0 and len(jobs["running"]) == 0

def get_all_schedule_job():
    #
    # curl http://localhost:6800/listjobs.json?project=journal | python3 -m json.tool
    #
    list_jobs_request = requests.get(LIST_JOB_RESOURCE)
    return list_jobs_request.json()

def get_pending_schedule_job():
    #
    # curl http://localhost:6800/listjobs.json?project=journal | python3 -m json.tool
    #
    list_jobs_request = requests.get(LIST_JOB_RESOURCE)
    value = list_jobs_request.json()
    return value["pending"]

def get_finished_schedule_job():
    #
    # curl http://localhost:6800/listjobs.json?project=journal | python3 -m json.tool
    #
    list_jobs_request = requests.get(LIST_JOB_RESOURCE)
    value = list_jobs_request.json()
    return value["finished"]

def get_running_schedule_job():
    #
    # curl http://localhost:6800/listjobs.json?project=journal | python3 -m json.tool
    #
    list_jobs_request = requests.get(LIST_JOB_RESOURCE)
    value = list_jobs_request.json()
    return value["running"]


##########################


def request_crawling_for_category(category: str):
    #
    # curl http://localhost:6800/schedule.json -d project=journal -d spider=categories -d category={0} | python3 -m json.tool
    #
    payload = [
        ('project', 'journal'), 
        ('spider', 'categories'), 
        ('category', category)
    ]

    request_schedule = requests.post(SCHEDULE_RESOURCE, data=payload)
    json_id = request_schedule.json()
    #send_message(json_id)


def request_crawling_for_front_page():
    #
    # curl http://localhost:6800/schedule.json -d project=journal -d spider=frontpage | python3 -m json.tool
    #
    payload = [
        ('project', 'journal'), 
        ('spider', 'frontpage')
    ]
    request_schedule = requests.post(SCHEDULE_RESOURCE, data=payload)
    json_id = request_schedule.json()
    #send_message(json_id)


def request_crawling_for_article(article_path: str):
    payload = [
        ('project', 'journal'), 
        ('spider', 'article'), 
        ('path', article_path)
    ]
    request_schedule = requests.post(SCHEDULE_RESOURCE, data=payload)
    json_id = request_schedule.json()
    #send_message(json_id)