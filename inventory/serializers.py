from rest_framework import serializers
from .models import Warehouse, Stock, ProductPrice, StockTransaction
from catalog.models import Product, Variant  # Assuming products & variants are in catalog app

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'slug', 'city', 'state', 'country', 'address', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def validate_name(self, value):
        qs = Warehouse.objects.exclude(id=self.instance.id) if self.instance else Warehouse.objects.all()
        if qs.filter(name=value).exists():
            raise serializers.ValidationError("A warehouse with this name already exists.")
        return value

class StockSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(write_only=True)
    variant_slug = serializers.SlugField(write_only=True, required=False)
    warehouse_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'product_slug', 'variant_slug', 'warehouse_slug', 'quantity', 'reserved_quantity',
                  'min_quantity', 'max_quantity', 'slug', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Fetch related objects
        try:
            validated_data['product'] = Product.objects.get(slug=validated_data.pop('product_slug'))
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        variant_slug = validated_data.pop('variant_slug', None)
        if variant_slug:
            try:
                validated_data['variant'] = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        try:
            validated_data['warehouse'] = Warehouse.objects.get(slug=validated_data.pop('warehouse_slug'))
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle related object updates
        product_slug = validated_data.pop('product_slug', None)
        if product_slug:
            try:
                instance.product = Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        variant_slug = validated_data.pop('variant_slug', None)
        if variant_slug:
            try:
                instance.variant = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        warehouse_slug = validated_data.pop('warehouse_slug', None)
        if warehouse_slug:
            try:
                instance.warehouse = Warehouse.objects.get(slug=warehouse_slug)
            except Warehouse.DoesNotExist:
                raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})

        return super().update(instance, validated_data)

class ProductPriceSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(write_only=True)
    variant_slug = serializers.SlugField(write_only=True, required=False)
    warehouse_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = ProductPrice
        fields = ['id', 'product_slug', 'variant_slug', 'warehouse_slug', 'price', 'compare_at_price',
                  'cost_price', 'currency', 'slug', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Resolve related objects
        try:
            validated_data['product'] = Product.objects.get(slug=validated_data.pop('product_slug'))
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        variant_slug = validated_data.pop('variant_slug', None)
        if variant_slug:
            try:
                validated_data['variant'] = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        try:
            validated_data['warehouse'] = Warehouse.objects.get(slug=validated_data.pop('warehouse_slug'))
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        product_slug = validated_data.pop('product_slug', None)
        if product_slug:
            try:
                instance.product = Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        variant_slug = validated_data.pop('variant_slug', None)
        if variant_slug:
            try:
                instance.variant = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        warehouse_slug = validated_data.pop('warehouse_slug', None)
        if warehouse_slug:
            try:
                instance.warehouse = Warehouse.objects.get(slug=warehouse_slug)
            except Warehouse.DoesNotExist:
                raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})

        return super().update(instance, validated_data)

class StockTransactionSerializer(serializers.ModelSerializer):
    stock_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = StockTransaction
        fields = ['id', 'stock_id', 'type', 'quantity', 'reference', 'slug', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            validated_data['stock'] = Stock.objects.get(id=validated_data.pop('stock_id'))
        except Stock.DoesNotExist:
            raise serializers.ValidationError({'stock_id': 'Invalid stock ID.'})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        stock_id = validated_data.pop('stock_id', None)
        if stock_id:
            try:
                instance.stock = Stock.objects.get(id=stock_id)
            except Stock.DoesNotExist:
                raise serializers.ValidationError({'stock_id': 'Invalid stock ID.'})
        return super().update(instance, validated_data)
