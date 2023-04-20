from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from django.template.loader import render_to_string
from django.conf import settings
from .models import Category, Author, Post
import requests
from django.contrib.auth.models import User
from celery import shared_task

from .models import PostCategory

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.header, subscribers)

@shared_task
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        author = instance.post_author
        subscribers = author.subscribers.all()
        subscribers = [s.email for s in subscribers]

        send_notifications_about_author_post(instance.preview(), instance.pk, instance.header, subscribers)

@shared_task
def send_notifications_about_author_post(preview, pk, title, subscribers):
    html_content = render_to_string(
        'author_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(username=instance)