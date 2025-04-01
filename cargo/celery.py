import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cargo.settings')

celery_app = Celery('cargo')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule = {
    'deactivate_expired_subscriptions_daily_at_8am': {
        'task': 'subscriptions.tasks.deactivate_expired_subscriptions',
        'schedule': crontab(minute=0, hour=8), 
    },
}