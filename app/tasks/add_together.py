import time
from . import celery


@celery.task()
def add_together(a, b):
    time.sleep(20)
    print(a + b)
    return a + b
