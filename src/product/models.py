from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import pre_save
from decimal import Decimal
from product.constants import CATEGORIES as categories


class Product(models.Model):
    name = models.CharField(max_length=120)
    manufacturer = models.CharField(max_length=80)
    category = models.CharField(max_length=40, choices=categories)
    model = models.CharField(max_length=80, null=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    specifications = models.TextField(blank=True, null=True)
    stock = models.IntegerField()
    discount = models.IntegerField(null=True)
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="date updated"
    )
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_total_price(self):
        discount = self.discount if self.discount else 0
        discount_amount = self.price * discount / 100
        stringified = str(Decimal(self.price) - Decimal(discount_amount))
        end_index = stringified.index(".")+3
        return stringified[:end_index] if "." in stringified else stringified


def pre_save_product_receiver(sender, instance, *args, **kwargs):

    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_product_receiver, sender=Product)
