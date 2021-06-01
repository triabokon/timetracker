from celery.decorators import task
from celery.utils.log import get_task_logger

from .utils import make_task_report, send_email

logger = get_task_logger(__name__)


@task(name="send_emails_task", queue="email")
def send_emails_task(emails, subject, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent emails")
    return send_email(emails, subject, message)


@task(name="send_task_report", queue="task_report")
def send_task_report(user_id, user_username, user_email):
    """makes user task report"""
    logger.info("Creating report")
    return make_task_report(user_id, user_username, user_email)
