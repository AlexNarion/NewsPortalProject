import datetime

import celery
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string

from .models import Category, Post
from django.core.mail import EmailMultiAlternatives


@shared_task
def get_week_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(addtime__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True)
    html_content = render_to_string(
        'daily_post.html',
        {
            'link':settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()