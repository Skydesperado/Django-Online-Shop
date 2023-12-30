from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand

from users.models import OTP


class Command(BaseCommand):
    help = "Remove Expired OTP Codes"

    def handle(self, *args, **options):
        expired_time = datetime.now(
            tz=pytz.timezone("Asia/Tehran")) - timedelta(minutes=2)
        OTP.objects.filter(created_at__lt=expired_time).delete()
        self.stdout.write(f"{OTP.objects.count()} Expired Records Removed")
