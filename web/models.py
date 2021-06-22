from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import decimal
import datetime
# Create your models here.
class Customer(models.Model):
    company = models.CharField(verbose_name='Nama Perusahaan', max_length=200)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(verbose_name="Alamat")
    city = models.CharField(max_length=200, verbose_name='Kota')
    provinz = models.CharField(max_length=200, verbose_name='Provinsi')
    phone = models.CharField(max_length=200, verbose_name='Telefon', null=True, blank=True)
    fax = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    terms = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['company']

    def __str__(self):
        return self.company

class Sales(models.Model):
    name = models.CharField(verbose_name='Nama', max_length=200)
    address = models.TextField(verbose_name="Alamat")
    phone = models.CharField(max_length=200, verbose_name='Telefon')
    starting_date = models.DateField(verbose_name='Mulai Kerja', null=False, blank=False)

    class Meta:
            ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(verbose_name='Nama', max_length=200)
    code = models.CharField(verbose_name='Kode Kategori', max_length=200)

    def __str__(self):
        return self.name

class DeliveryOrder(TimeStampedModel):
    class Meta:
        verbose_name = 'Surat Jalan'

    customer = models.ForeignKey(Customer, related_name='delivery_orders', on_delete=models.SET_NULL, null=True, blank=True)
    sales = models.ForeignKey(Sales, related_name='delivery_orders', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_order_date = models.DateField(verbose_name="Tanggal Kirim")
    added_by = models.ForeignKey(User, related_name='delivery_orders', on_delete=models.CASCADE)
    pic = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='delivery_orders', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.customer.company


class Product(models.Model):
    delivery_order = models.ForeignKey(DeliveryOrder, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nama Produk', max_length=200)
    quantity = models.PositiveIntegerField() 
    metric_type = models.CharField(verbose_name='Ukuran (roll, pcs)', max_length=200, null=True, blank=True) # roll, kg, pcs
    unit_quantity = models.PositiveIntegerField(null=True, blank=True)
    unit_metric = models.CharField(verbose_name='Satuan Unit (M, KG)', max_length=200, null=True, blank=True) # roll, kg, pcs

    @property
    def total(self):
        if self.unit_quantity:
            return self.quantity * self.unit_quantity
        else:
            return self.quantity

    def __str__(self):
        if self.unit_quantity:
            return "{quantity} {metric_type} {name} @ {unit_quantity} M".format(quantity=self.quantity, metric_type=self.metric_type, name=self.name, unit_quantity=self.unit_quantity )
        else:
            return "{quantity} {metric_type} {name} ".format(quantity=self.quantity, metric_type=self.metric_type, name=self.name )


class Invoice(TimeStampedModel):
    delivery_order = models.ForeignKey(DeliveryOrder, verbose_name="Surat Jalan", on_delete=models.CASCADE, related_name='invoices')
    discount = models.PositiveIntegerField(default=0, null=True, blank=True)
    sales_tax = models.PositiveIntegerField(default=0, null=True, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    delivery_cost = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    #sub_total = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    rounded = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    #pic = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return "{0} - {1}".format(self.delivery_order.id, self.created.date())

    @property
    def number(self):
        return "{0}/{1}/{2}".format(self.delivery_order.id, "KBS", self.created.year )

class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=200)
    discount = models.PositiveIntegerField(default=0,null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=True, blank=True)
    metric_type = models.CharField(null=True, blank=True, max_length=20)
    
    def __str__(self):
        return "{0} - {1}".format(self.invoice.id, self.description)

   
    @property
    def total(self):
        sub = self.quantity * self.unit_price
        discount =  sub * decimal.Decimal((self.discount/100))
        return round(sub - discount,2)

@receiver(post_save, sender=DeliveryOrder)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        Invoice.objects.create(delivery_order=instance)

@receiver(post_save, sender=Product)
def add_invoice_item(sender, instance, created, **kwargs):
    if created:
        invoice = Invoice.objects.get(delivery_order=instance.delivery_order)
        InvoiceItem.objects.create(invoice=invoice, product=instance, quantity=instance.quantity, description=instance.name)
    
@receiver(post_delete, sender=Product)
def delete_invoice_item(sender, instance, **kwargs):
    try:
        invoice_item = InvoiceItem.objects.get(product=instance)
        invoice_item.delete()
    except Exception as error:
        return