from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.urls import reverse
from django.dispatch import receiver
from product.models import Product
from customer.models import Customer


class Cart(models.Model):
    
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(Product, through='CartItem')
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="creation date", auto_now_add=True)
    
    def __str__(self):
        return f'{self.date_created}-{self.customer}-{self.account}'
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def get_absolute_url(self):
        return reverse("carts:cart-detail", kwargs={"id": self.id})

# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)


# pre_save.connect(pre_save_cart_receiver, sender=Cart)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.SET_DEFAULT, default=None)
    quantity = models.IntegerField()