from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import SubscriptionPlan

@receiver([post_save, post_delete], sender=SubscriptionPlan)
def invalidate_sub_plans_cache(sender, instance, created, **kwargs):
    cache_key = 'sub_plans'  

    cache.delete_pattern(cache_key)
