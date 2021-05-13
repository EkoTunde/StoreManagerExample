from django.db import models
from django.conf import settings
from django.urls import reverse
from product.models import Product
from customer.models import Customer


class Cart(models.Model):

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+',
        default=None
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        default=None
    )
    products = models.ManyToManyField(Product, through='CartItem')
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(
        verbose_name="creation date",
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.date_created}-{self.customer}-{self.account}'

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def get_absolute_url(self):
        return reverse("carts:cart-detail", kwargs={"id": self.id})

    def get_add_product_url(self):
        return reverse("carts:cart-detail"+"/add", kwargs={"id": self.id})

# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.name)


# pre_save.connect(pre_save_cart_receiver, sender=Cart)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_DEFAULT, default=None)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_DEFAULT,
        default=None
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity}-{self.cart}-{self.product}'

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


def get_product_queryset(cart=None):
    products = cart.products.all()
    number_of_products = len(products)
    print(number_of_products)
    return None
