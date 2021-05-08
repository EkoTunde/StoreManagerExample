from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from product.constants import CATEGORIES as categories


class Product(models.Model):
    name = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=80)
    category = models.CharField(max_length=40, choices=categories)
    model = models.CharField(max_length=80, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    specifications = models.TextField(blank=True, null=True)
    stock = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    date_updated = models.DateTimeField(auto_now=
             True, verbose_name="date updated")
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


def pre_save_product_receiver(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_product_receiver, sender=Product)
