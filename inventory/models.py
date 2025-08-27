import uuid
from django.db import models
from django.utils.text import slugify
from catalog.models import Product, Variant


class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Warehouse.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True, related_name='stock')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0)
    reserved_quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ('product', 'variant', 'warehouse')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.product.name}-{self.variant or 'default'}-{self.warehouse.name}")
            slug = base_slug
            counter = 1
            while Stock.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.variant or 'Default'} @ {self.warehouse.name}"

class ProductPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True, related_name='prices')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True, related_name='prices')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=5, default='USD')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Price"
        verbose_name_plural = "Product Prices"
        unique_together = ('product', 'variant', 'warehouse')

    def save(self, *args, **kwargs):
        if not self.slug:
            target = self.variant or self.product
            location = self.warehouse.name if self.warehouse else 'global'
            base_slug = slugify(f"{target}-{location}-price")
            slug = base_slug
            counter = 1
            while ProductPrice.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        target = self.variant or self.product
        location = self.warehouse.name if self.warehouse else "Global"
        return f"{target} - {location} Price: {self.price} {self.currency}"

class StockTransaction(models.Model):
    TYPE_ADJUSTMENT = 'adjustment'
    TYPE_SALE = 'sale'
    TYPE_RETURN = 'return'
    TYPE_TRANSFER = 'transfer'

    TRANSACTION_CHOICES = [
        (TYPE_ADJUSTMENT, 'Stock Adjustment'),
        (TYPE_SALE, 'Sale'),
        (TYPE_RETURN, 'Return'),
        (TYPE_TRANSFER, 'Transfer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    quantity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stock Transaction"
        verbose_name_plural = "Stock Transactions"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.stock}-{self.type}-{self.quantity}")
            slug = base_slug
            counter = 1
            while StockTransaction.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} - {self.quantity} units for {self.stock}"
