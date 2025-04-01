from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Content

@receiver([post_save, post_delete], sender = Content )
def invalidate_contents_list_cache(sender, instance, created, **kwargs):
    cache.delete_pattern('contents_list')

