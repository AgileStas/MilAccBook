"""
Definition of models.
"""

from random import choices
from sre_constants import CATEGORY_DIGIT
from django.db import models

class Peer(models.Model):
    name = models.CharField(max_length=200)

PRODUCT_UNIT_OF_MEASURE = (
    (1, "Kilogramm"), # Кілограм
    (2, "Piece"),     # Штука
    (3, "Kit"),       # Комплект
    (4, "Box"),       # Коробка
    (5, "Pack"),      # Пачка
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
    #total_q = models.FloatField()
    #sort1_q = models.FloatField()
    #sort2_q = models.FloatField()
    #sort3_q = models.FloatField()
    #sort4_q = models.FloatField()
    #sort5_q = models.FloatField()

    #def __init__(self):
    #    self.total_q = 0.0
    #    self.sort1_q = 0.0
    #    self.sort2_q = 0.0
    #    self.sort3_q = 0.0
    #    self.sort4_q = 0.0
    #    self.sort5_q = 0.0

    def __init__(self, total_q=0.0, sort1_q=0.0, sort2_q=0.0, sort3_q=0.0, sort4_q=0.0, sort5_q=0.0):
        self.total_q = total_q
        self.sort1_q = sort1_q
        self.sort2_q = sort2_q
        self.sort3_q = sort3_q
        self.sort4_q = sort4_q
        self.sort5_q = sort5_q

    def increase(self, value):
        #print('+++ (' + str(self.total_q) + '+' + str(value.total_q) + ')=(' + str(self.sort1_q) + '+' + str(value.sort1_q) + ')+(' + str(self.sort2_q) + '+' + str(value.sort2_q) + ')+(' + str(self.sort3_q) + '+' + str(value.sort3_q) + ')+(' + str(self.sort4_q) + '+' + str(value.sort4_q) + ')+(' + str(self.sort5_q) + '+' + str(value.sort5_q) + ')')
        self.total_q += value.total_q
        self.sort1_q += value.sort1_q
        self.sort2_q += value.sort2_q
        self.sort3_q += value.sort3_q
        self.sort4_q += value.sort4_q
        self.sort5_q += value.sort5_q

        return self

    def decrease(self, value):
        #print('--- (' + str(self.total_q) + '-' + str(value.total_q) + ')=(' + str(self.sort1_q) + '-' + str(value.sort1_q) + ')+(' + str(self.sort2_q) + '-' + str(value.sort2_q) + ')+(' + str(self.sort3_q) + '-' + str(value.sort3_q) + ')+(' + str(self.sort4_q) + '-' + str(value.sort4_q) + ')+(' + str(self.sort5_q) + '-' + str(value.sort5_q) + ')')
        self.total_q -= value.total_q
        self.sort1_q -= value.sort1_q
        self.sort2_q -= value.sort2_q
        self.sort3_q -= value.sort3_q
        self.sort4_q -= value.sort4_q
        self.sort5_q -= value.sort5_q

        return self

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

    @property
    def operation_q(self):
        return ComplexQuantity(total_q=self.total_q, sort1_q=self.sort1_q, sort2_q=self.sort2_q, sort3_q=self.sort3_q, sort4_q=self.sort4_q, sort5_q=self.sort5_q)
    
    #   set { TotalQuantity = value.TotalQuantity; Sort1Quantity = value.Sort1Quantity; Sort2Quantity = value.Sort2Quantity; Sort3Quantity = value.Sort3Quantity; Sort4Quantity = value.Sort4Quantity; Sort5Quantity = value.Sort5Quantity; }

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

    @property
    def operation_q(self):
        return ComplexQuantity(total_q=self.total_q, sort1_q=self.sort1_q, sort2_q=self.sort2_q, sort3_q=self.sort3_q, sort4_q=self.sort4_q, sort5_q=self.sort5_q)
    #   set { TotalQuantity = value.TotalQuantity; Sort1Quantity = value.Sort1Quantity; Sort2Quantity = value.Sort2Quantity; Sort3Quantity = value.Sort3Quantity; Sort4Quantity = value.Sort4Quantity; Sort5Quantity = value.Sort5Quantity; }

class JournalLine(models.Model):
    record_date = models.DateField()
    document_product = models.ForeignKey(DocumentProduct, on_delete=models.CASCADE)
    
