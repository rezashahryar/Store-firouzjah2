from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.utils.text import slugify

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


@receiver(pre_save, sender=Product)
def create_product(instance, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance)


def create_unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.base_product.title_farsi, allow_unicode=True)
    
    instance_class = instance.__class__
    queryset = instance_class.objects.filter(slug=slug)

    if queryset.exists():
        new_slug = f'{slug}-{queryset.first().id}'
        return create_unique_slug(instance, new_slug)
    return slug
