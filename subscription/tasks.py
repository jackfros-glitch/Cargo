from celery import shared_task
from django.utils import timezone
from .models import Subscription

@shared_task
def deactivate_expired_subscriptions():
    now = timezone.now()
    expired_subscriptions = Subscription.objects.filter(end_date__lt=now, auto_renew=False)
    
    for sub in expired_subscriptions:
        sub.delete() 

    return f"Deactivated {expired_subscriptions.count()} expired subscriptions."
