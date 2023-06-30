from django.contrib.postgres.fields import ArrayField
from django.db import models


class ChemicalProduct(models.Model):
    class Unit(models.TextChoices):
        MILLIGRAM = "mg"
        GRAM = "g"
        KILOGRAM = "kg"
        PACK = "pack"
        MILLILITER = "ml"
        LITER = "l"

    company_name = models.CharField(max_length=255)
    product_url = models.URLField(max_length=1024)
    collected_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField()
    numcas = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    qt_list = ArrayField(models.IntegerField(), size=5)
    unit_list = ArrayField(models.CharField(choices=Unit.choices, max_length=8), size=5)
    currency_list = ArrayField(models.CharField(max_length=32), size=5)
    price_pack_list = ArrayField(models.IntegerField(), size=5)

    class Meta:
        verbose_name = "Chemical Product"
        verbose_name_plural = "Chemical Products"
