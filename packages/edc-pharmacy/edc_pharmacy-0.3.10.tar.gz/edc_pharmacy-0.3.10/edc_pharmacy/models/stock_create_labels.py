from uuid import uuid4

from django.db import models
from django.db.models import PROTECT
from edc_model.models import BaseUuidModel, HistoricalRecords

from .product import Product


class Manager(models.Manager):
    use_in_migrations = True


class StockCreateLabels(BaseUuidModel):
    product = models.ForeignKey(Product, on_delete=PROTECT)

    qty = models.IntegerField(verbose_name="Number of labels to print")

    printed = models.BooleanField(default=False)

    printed_datetime = models.DateTimeField(null=True, blank=True)

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.product}: {self.qty} "

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Medication stock: Create labels"
        verbose_name_plural = "Medication stock: Create labels"


class Labels(BaseUuidModel):
    stock_create_labels = models.ForeignKey(StockCreateLabels, on_delete=PROTECT)

    stock_identifier = models.CharField(max_length=36, default=uuid4, unique=True)

    printed = models.BooleanField(default=False)

    printed_datetime = models.DateTimeField(null=True, blank=True)

    in_stock = models.BooleanField(default=False)

    in_stock_datetime = models.DateTimeField(null=True, blank=True)

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.stock_labels}: {self.stock_identifier} "

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Label"
        verbose_name_plural = "Labels"
