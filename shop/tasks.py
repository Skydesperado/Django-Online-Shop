from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from utilities.bucket import bucket

from .models import Order

logger = get_task_logger(__name__)


def get_bucket_objects_task():
    objects = bucket.get_bucket_objects()
    return objects


@shared_task
def download_bucket_object_task(key):
    bucket.download_bucket_object(key)


@shared_task
def delete_bucket_object_task(key):
    bucket.delete_bucket_object(key)


@shared_task
def delete_unpaid_orders_task():
    try:
        unpaid_orders = Order.objects.filter(is_paid=False,
                                             created_at__lte=timezone.now() -
                                             timedelta(hours=12))
        for order in unpaid_orders:
            order.delete()
        logger.info(f"Deleted {len(unpaid_orders)} Unpaid Orders")
    except Exception as exception:
        logger.error(f"An Error Occurred: {exception}")
