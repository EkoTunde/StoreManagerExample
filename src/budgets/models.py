from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from customer.models import Customer
from product.models import Product

class Budget(models.Model):
    
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(Product)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="creation date", auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)
    
    def __str__(self):
        return self.date_created + " " + self.customer
    
    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_product_receiver, sender=Product)