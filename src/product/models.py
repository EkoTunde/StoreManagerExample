from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


CATEGORIES = [
    ("Electronics & Office", "Electronics & Office"),
    ("Clothing, Shoes & Accessories", "Clothing, Shoes & Accessories"),
    ("Home, Furniture & Appliances", "Home, Furniture & Appliances"),
    ("Toys, Games, and Video Games", "Toys, Games, and Video Games"),
    ("Home Improvement", "Home Improvement"),
    ("Movies, Music & Books", "Movies, Music & Books"),
    ("Baby", "Baby"),
    ("Patio & Garden", "Patio & Garden"),
    ("Food, Household & Pets", "Food, Household & Pets"),
    ("Pharmacy, Health & Personal Care", "Pharmacy, Health & Personal Care"),
    ("Beauty", "Beauty"),
    ("Sports, Fitness & Outdoors", "Sports, Fitness & Outdoors"),
    ("Auto, Tires & Industrial", "Auto, Tires & Industrial"),
    ("Photo & Personalized Shop", "Photo & Personalized Shop"),
    ("Art, Craft, Sewing & Party Supplies", "Art, Craft, Sewing & Party Supplies"),
]


class Product(models.Model):
    name = models.CharField(max_length=80)
    manufacturer = models.CharField(max_length=80)
    category = models.CharField(max_length=40, choices=CATEGORIES)
    model = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    specifications = models.TextField(max_length=9999)
    stock = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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
