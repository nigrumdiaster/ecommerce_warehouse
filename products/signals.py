from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Product
from .services import product_lookup_service


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_lookup(sender, instance, **kwargs):
    product_lookup_service.invalidate()