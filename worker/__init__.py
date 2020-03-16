import os

from celery import Celery

from worker import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tiger.settings")


celery_app = Celery('tiger')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()


def call_by_worker(func):
    '''在 celery 中任务进行异步调用'''
    task = celery_app.task(func)
    return task.delay
