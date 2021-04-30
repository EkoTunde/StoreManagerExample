from django.db import models


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