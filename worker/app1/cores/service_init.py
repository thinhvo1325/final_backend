from redis import Redis
from decouple import config 

# redis = Redis(
#     host=config('REDIS_HOST'), 
#     port=config('REDIS_PORT'), 
#     # password=config.REDIS['pass'],
#     db=config('REDIS_DB')
# )

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



#----------------------CHECKER INFORMATION------------------------------------
def is_backend_running() -> bool:
    try:
        redis_connecter = Redis(
            host='localhost', 
            port=config('REDIS_PORT'), 
            password='password', 
            db=config('REDIS_DB')
        )
        redis_connecter.client_list()  # Must perform an operation to check connection.
        print(22222222222222222222222222222222222222222222)
    except ConnectionError as e:
        print("Failed to connect to Redis instance at")
        print(repr(e))
        return False
    # redis_connecter.close()
    return True

from kombu import Connection
from kombu.exceptions import OperationalError
def is_broker_running(retries: int = 3) -> bool:
    try:
        conn = Connection(CELERY_BROKEN_URL)
        conn.ensure_connection(max_retries=retries)
        print(1111111111111111111111111111111111)
    except OperationalError as e:
        print("Failed to connect to RabbitMQ instance at ")
        print(str(e))
        return False
    conn.close()
    return True