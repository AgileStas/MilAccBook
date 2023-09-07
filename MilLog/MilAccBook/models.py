"""
Definition of models.
"""

from random import choices
from sre_constants import CATEGORY_DIGIT
from django.db import models

class Peer(models.Model):
    name = models.CharField(max_length=200)

PRODUCT_UNIT_OF_MEASURE = (
    (1, "Kilogramm"), # кілограм
    (2, "Piece"),     # штука
    (3, "Kit"),       # комплект
    (4, "Box"),       # коробка
    (5, "Pack"),      # пачка
    )    
class Product(models.Model):
    name = models.CharField(max_length=200)
    has_sort = models.BooleanField()
    uom = models.IntegerField(choices=PRODUCT_UNIT_OF_MEASURE)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    # sort = models.IntegerField()

class ComplexQuantity:
    total_q = models.FloatField()
    sort1_q = models.FloatField()
    sort2_q = models.FloatField()
    sort3_q = models.FloatField()
    sort4_q = models.FloatField()
    sort5_q = models.FloatField()
    
    #def increase
    #def decrease

COMPLEX_OPERATION = 1
EXTERNAL_TRANSFER = 2
INTERNAL_TRANSFER = 3
CATEGORY_CHANGE = 4
OPERATION_TYPE = (
        (COMPLEX_OPERATION, "Complex operation"),
        (EXTERNAL_TRANSFER, "External transfer"),
        (INTERNAL_TRANSFER, "Internal transfer"),
        (CATEGORY_CHANGE, "Category change")
    )
class Document(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    date = models.DateField()
    operation = models.IntegerField(choices=OPERATION_TYPE)
    peer = models.ForeignKey(Peer, on_delete=models.CASCADE)
    base_document = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    base_document_str = models.CharField(max_length=200, null=True)

class DocumentProduct(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

    total_q = models.FloatField()
    sort1_q = models.FloatField(default=0)
    sort2_q = models.FloatField(default=0)
    sort3_q = models.FloatField(default=0)
    sort4_q = models.FloatField(default=0)
    sort5_q = models.FloatField(default=0)
    #def operation_quantity

    #    public virtual ICollection<OperationSubline> OperationSublines { get; private set; } =
    #        new ObservableCollection<OperationSubline>();

class OperationSubline(models.Model):
    operation = models.IntegerField(choices=OPERATION_TYPE)
    peer = models.ForeignKey(Peer, on_delete=models.CASCADE)
    document_product = models.ForeignKey(DocumentProduct, on_delete=models.CASCADE)

    total_q = models.FloatField()
    sort1_q = models.FloatField(default=0)
    sort2_q = models.FloatField(default=0)
    sort3_q = models.FloatField(default=0)
    sort4_q = models.FloatField(default=0)
    sort5_q = models.FloatField(default=0)
    #def operation_quantity

class JournalLine(models.Model):
    record_date = models.DateField()
    document_product = models.ForeignKey(DocumentProduct, on_delete=models.CASCADE)
    