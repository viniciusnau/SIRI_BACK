import os
from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail

from stock.models import Protocol


@shared_task
def verify_end_date():
    today = datetime.now().date()
    ninety_days_later = today + timedelta(days=90)
    protocols = Protocol.objects.filter(end_date__date=ninety_days_later)
    admins = User.objects.filter(is_superuser=True)
    recipient_list = admins.values_list("email", flat=True)
    from_email = os.environ.get("EMAIL_HOST_USER")
    protocol_codes = [protocol.code for protocol in protocols]
    protocol_codes_str = "\n".join(protocol_codes)

    if protocols:
        send_mail(
            "Alerta Final de Vingência de Ata",
            f"Os seguintes protocolos estão a noventa dias do final de suas vingências:\n{protocol_codes_str}",
            from_email,
            recipient_list,
            fail_silently=False,
        )
