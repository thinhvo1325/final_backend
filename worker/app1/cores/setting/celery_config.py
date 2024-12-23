"""Module with Celery configurations to Audio Length worker."""
from kombu import Queue
from decouple import config 


#=========================================================================
#                          CELERY INFORMATION 
#=========================================================================

# Set worker to ack only when return or failing (unhandled expection)
task_acks_late = True

# Worker only gets one task at a time
worker_prefetch_multiplier = 1

QUERY_NAME = config('QUEUE_TEXT_DETECTION')

# Create queue for worker
task_queues = [Queue(name=QUERY_NAME)]

# Set Redis key TTL (Time to live)
result_expires = 60 * 60 * 48  # 48 hours in seconds