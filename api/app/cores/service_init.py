from redis import Redis
from decouple import config
from celery import Celery

#----------------------REDIS INFORMATION------------------------------------
redis_connecter = Redis(
    host=config('REDIS_HOST'), 
    port=config('REDIS_PORT'), 
    password=config('REDIS_PASSWORD'), 
    db=config('REDIS_DB')
)

#----------------------CELERY INFORMATION------------------------------------
CELERY_BROKEN_URL = "amqp://{user}:{pw}@{hostname}:{port}/{vhost}".format(
    user=config('RABBITMQ_USERNAME'), 
    pw=config('RABBITMQ_PASSWORD'), 
    hostname=config('RABBITMQ_HOST'), 
    port=config('RABBITMQ_PORT'), 
    vhost=config('RABBITMQ_HOST')
)

CELERY_BACKED_URL = "redis://:password@{hostname}:{port}/{db}".format(
    hostname=config('REDIS_HOST'),
    port=config('REDIS_PORT'),
    db=config('REDIS_DB'),
)

celery_execute = Celery(
    broker=CELERY_BROKEN_URL,
    backend=CELERY_BACKED_URL
)

