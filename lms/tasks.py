from celery import shared_task
from django.core.mail import send_mail

from config import settings
from lms.models import Course, Subscription


@shared_task
def send_email_task(course):
    subscription = Subscription.objects.filter(course=course)
    if subscription:
        course_name = subscription[0].course.title
        emails = []
        for sub in subscription:
            emails.append(sub.user.email)
            send_mail(f'обновление курса {course_name}. По вашей подписке вышел новый урок',
                      settings.EMAIL_HOST_USER, emails)
