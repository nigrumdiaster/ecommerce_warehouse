from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Product, Category
from .services import product_lookup_service


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_lookup(sender, instance, **kwargs):
    product_lookup_service.invalidate()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_lookup(sender, instance, **kwargs):
    product_lookup_service.invalidate()
