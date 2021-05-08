from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.text import slugify


class Customer(models.Model):
    
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    doc_id = models.IntegerField()
    address = models.CharField(max_length=80)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone = models.IntegerField()
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


def pre_save_customer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.doc_id)


pre_save.connect(pre_save_customer_receiver, sender=Customer)