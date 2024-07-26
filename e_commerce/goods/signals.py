from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product
from django.conf import settings


cache_key = settings.CACHE_NAME

@receiver(post_save, sender=Product)
def clear_cache_on_save(sender, instance, **kwargs):
    """If any product in the list is changed, the cache is cleared"""
    cache.delete(cache_key)

@receiver(post_delete, sender=Product)
def clear_cache_on_delete(sender, instance, **kwargs):
    """If a product was deleted, the cache is cleared"""
    cache.delete(cache_key)