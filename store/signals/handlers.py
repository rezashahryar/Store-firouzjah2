from django.dispatch import receiver
from django.db.models.signals import post_save

from store.models import Product, SimilarProduct

# create your signals here


@receiver(post_save, sender=Product)
def create_similar_product_when_add_new_product(created, instance, **kwargs):
    if created:
        SimilarProduct.objects.create(
            store_id=instance.base_product.store.pk,
            product_id=instance.pk
        )
