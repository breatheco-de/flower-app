from __future__ import absolute_import, unicode_literals

# the rest of your Celery file contents go here
import os
# from datetime import UTC, datetime, timedelta
# from typing import TypedDict

from celery import Celery
# from celery.signals import worker_process_init

# from .setup import get_redis_config

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "breathecode.settings")

# django.setup()

# settings, kwargs, REDIS_URL = get_redis_config()
kwargs = {}
ENV_KEY = os.getenv("RMQ_URL_KEY", "CLOUDAMQP_URL")
CLOUDAMQP_URL = os.getenv(ENV_KEY, "")

# Decide SSL usage by checking the scheme
if CLOUDAMQP_URL.startswith("amqps://"):
    # Convert 'amqps://' to 'pyamqp://'
    BROKER_URL = CLOUDAMQP_URL.replace("amqps://", "pyamqp://", 1)
    BROKER_USE_SSL = True
else:
    # Convert 'amqp://' to 'pyamqp://'
    BROKER_URL = CLOUDAMQP_URL.replace("amqp://", "pyamqp://", 1)
    BROKER_USE_SSL = False

app = Celery("celery_breathecode", **kwargs)
if os.getenv("ENV") == "test":
    app.conf.update(task_always_eager=True)

# if os.getenv("ENV") == "test" or not CLOUDAMQP_URL:
#     BROKER_URL = REDIS_URL

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.conf.update(
    broker_url=BROKER_URL,
    # result_backend=REDIS_URL,
    broker_use_ssl=BROKER_USE_SSL,
    namespace="CELERY",
    result_expires=10,
    worker_max_memory_per_child=int(os.getenv("CELERY_MAX_MEMORY_PER_WORKER", "470000")),
    worker_max_tasks_per_child=int(os.getenv("CELERY_MAX_TASKS_PER_WORKER", "1000")),
)

app.conf.broker_transport_options = {
    "priority_steps": list(range(11)),
    "sep": ":",
    "queue_order_strategy": "priority",
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
