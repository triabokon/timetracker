import csv
import io
import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.serializers.json import DjangoJSONEncoder

from .models import Task


def send_email(emails, subject, message):
    email = EmailMessage(
        subject,
        message,
        [settings.DEFAULT_FROM_EMAIL],
        emails,
        [],
    )
    return email.send(fail_silently=False)


def make_task_report(user_id, user_username, user_email):
    tasks = Task.objects.filter(owner_id=user_id)
    header = ['name', 'description', 'status', 'time_entries']
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(header)
    for t in tasks:
        writer.writerow(
            [
                t.name,
                t.description,
                t.status,
                json.dumps(
                    t.time_entries,
                    sort_keys=True,
                    indent=1,
                    cls=DjangoJSONEncoder,
                ),
            ]
        )

    email = EmailMessage(
        subject=f'{user_username} task report',
        from_email=[settings.DEFAULT_FROM_EMAIL],
        to=[user_email],
        bcc=[],
    )
    f.seek(0)
    email.attach(f'{user_username} task report', f.read())
    email.send(fail_silently=False)
    f.close()
    return None
