from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from store.models import Product, SimilarProduct, Customer

# create your signals here


@receiver(post_save, sender=Product)
def create_similar_product_when_add_new_product(created, instance, **kwargs):
    if created:
        SimilarProduct.objects.create(
            store_id=instance.base_product.store.pk,
            product_id=instance.pk
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(created, instance, *args, **kwargs):
    if created:
        Customer.objects.create(
            user_id=instance.pk
        )
