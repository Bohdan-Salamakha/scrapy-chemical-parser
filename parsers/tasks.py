from celery import shared_task


@shared_task()
def run_spider(spider_name: str):
    pass
