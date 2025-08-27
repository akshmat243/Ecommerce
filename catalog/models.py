import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.db.models import Index, JSONField
from decimal import Decimal


def generate_unique_slug(model, base):
    slug = slugify(base)[:200]
    counter = 1
    Model = model
    while Model.objects.filter(slug=slug).exists():
        slug = f"{slugify(base)[:190]}-{counter}"
        counter += 1
    return slug


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    image = models.ImageField(upload_to='category/%Y/%m/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            Index(fields=['slug']),
            Index(fields=['parent', 'name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name or str(uuid.uuid4()))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    logo = models.ImageField(upload_to='brand/%Y/%m/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        indexes = [Index(fields=['slug'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Brand, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    TYPE_TEXT = 'text'
    TYPE_INTEGER = 'integer'
    TYPE_DECIMAL = 'decimal'
    TYPE_BOOLEAN = 'boolean'
    TYPE_SELECT = 'select'
    TYPE_MULTI = 'multiselect'

    TYPE_CHOICES = [
        (TYPE_TEXT, 'Text'),
        (TYPE_INTEGER, 'Integer'),
        (TYPE_DECIMAL, 'Decimal'),
        (TYPE_BOOLEAN, 'Boolean'),
        (TYPE_SELECT, 'Select'),
        (TYPE_MULTI, 'MultiSelect'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_TEXT)
    unit = models.CharField(max_length=30, blank=True, null=True)
    is_variant_axis = models.BooleanField(default=False, help_text="If true this attribute is used to build variants (e.g. Size/Color).")
    is_filterable = models.BooleanField(default=True)
    ordering = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"
        indexes = [Index(fields=['slug']), Index(fields=['name'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Attribute, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    numeric_value = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    bool_value = models.BooleanField(null=True, blank=True) 
    hex_code = models.CharField(max_length=7, null=True, blank=True)  # for color hex
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ('attribute', 'value')
        indexes = [Index(fields=['attribute']), Index(fields=['value'])]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.attribute.name}-{self.value}"
            self.slug = generate_unique_slug(AttributeValue, base)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class Product(models.Model):
    TYPE_SIMPLE = 'simple'
    TYPE_VARIANT = 'variant_parent'
    TYPE_BUNDLE = 'bundle'

    TYPE_CHOICES = [
        (TYPE_SIMPLE, 'Simple'),
        (TYPE_VARIANT, 'Variant Parent'),
        (TYPE_BUNDLE, 'Bundle/Kit'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=120, unique=True, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SIMPLE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    weight_grams = models.PositiveIntegerField(null=True, blank=True)
    dimensions = JSONField(null=True, blank=True)  # {"length":mm,"width":mm,"height":mm}
    country_of_origin = models.CharField(max_length=2, null=True, blank=True)  # ISO2
    is_returnable = models.BooleanField(default=True)
    is_cod_allowed = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)  # free-form data
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            Index(fields=['slug']),
            Index(fields=['status']),
            Index(fields=['category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    Non-variant attributes attached to product for display & filtering.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value_text = models.CharField(max_length=255, blank=True, null=True)
    value_numeric = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('product', 'attribute')

    def __str__(self):
        return f"{self.product.name} — {self.attribute.name}"


class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)  # optional friendly name (e.g., "Red / M")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_code = models.CharField(max_length=50, blank=True, null=True)
    weight_grams = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
        indexes = [Index(fields=['sku']), Index(fields=['product'])]
    
    @property
    def stock_status(self):
        return "Active" if self.is_active else "Inactive"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.name or self.sku or str(uuid.uuid4())
            self.slug = generate_unique_slug(Variant, base)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"{self.product.name} — {self.sku}"


class VariantAttribute(models.Model):
    """
    Connects a variant to concrete attribute values (axes).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('variant', 'attribute')
        indexes = [Index(fields=['variant']), Index(fields=['attribute'])]

    def __str__(self):
        return f"{self.variant.sku} — {self.attribute.name}: {self.attribute_value.value}"


class ProductMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    media = models.ImageField(upload_to='product/%Y/%m/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Media"
        verbose_name_plural = "Product Media"
        indexes = [Index(fields=['product']), Index(fields=['variant']), Index(fields=['is_primary'])]

    def __str__(self):
        owner = self.variant or self.product
        return f"Media for {owner}"


class BundleItem(models.Model):
    """
    Items inside a Product bundle/kit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bundle = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bundle_items')
    child_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bundled_in')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    class Meta:
        verbose_name = "Bundle Item"
        verbose_name_plural = "Bundle Items"
        unique_together = ('bundle', 'child_product')

    def __str__(self):
        return f"{self.child_product.name} x {self.quantity} in {self.bundle.name}"
