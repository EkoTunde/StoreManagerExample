from django.db import models
from django.conf import settings
from product.models import Product
from customer.models import Customer

class Order(models.Model):
    
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="creation date", auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)
    
    def __str__(self):
        return self.date_created + " " + self.customer
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"