from redis import Redis
from decouple import config
from celery import Celery

#----------------------REDIS INFORMATION------------------------------------
redis_connecter = Redis(
    host='localhost', 
    port=9678, 
    password='password', 
    db=config('REDIS_DB')
)

#----------------------CELERY INFORMATION------------------------------------
CELERY_BROKEN_URL = "amqp://{user}:{pw}@{hostname}:{port}/{vhost}".format(
     user='guest', 
    pw='guest', 
    hostname='localhost', 
    port=9999, 
    vhost=config('RABBITMQ_HOST')
)

CELERY_BACKED_URL = "redis://:password@{hostname}:{port}/{db}".format(
    hostname=config('REDIS_HOST'),
    port=9678,
    db=config('REDIS_DB'),
)

celery_execute = Celery(
    broker=CELERY_BROKEN_URL,
    backend=CELERY_BACKED_URL
)

