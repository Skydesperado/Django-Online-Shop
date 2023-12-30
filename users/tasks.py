from datetime import datetime, timedelta

import pytz
from celery import shared_task

from users.models import OTP


@shared_task
def delete_expired_otps_task():
    expired_time = datetime.now(tz=pytz.timezone("Asia/Tehran")) - timedelta(
        minutes=2)
    OTP.objects.filter(created_at__lt=expired_time).delete()
