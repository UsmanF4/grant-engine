from celery.signals import worker_init
from app.core.config import settings
from app.db.database import get_db


celery = settings.celery
redis_client = settings.redis_client
loop = settings.loop


@worker_init.connect
def on_worker_init(**kwargs):
    loop.run_until_complete(get_db())
