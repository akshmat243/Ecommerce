from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceipt
from inventory.models import Warehouse
from catalog.models import Product, Variant

# ---------------- Supplier ----------------
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'slug', 'contact_person', 'email', 'phone', 'address', 'city', 'state', 'country', 'is_active']
        read_only_fields = ['id', 'slug']

    def validate_name(self, value):
        qs = Supplier.objects.exclude(id=self.instance.id) if self.instance else Supplier.objects.all()
        if qs.filter(name=value).exists():
            raise serializers.ValidationError("A supplier with this name already exists.")
        return value


# ---------------- PurchaseOrder ----------------
class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_slug = serializers.SlugField(write_only=True)
    warehouse_slug = serializers.SlugField(write_only=True)
    supplier = SupplierSerializer(read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'order_number', 'slug', 'supplier', 'supplier_slug',
            'warehouse_slug', 'warehouse', 'status', 'order_date', 
            'expected_delivery_date', 'total_amount', 'notes'
        ]
        read_only_fields = ['id', 'slug', 'supplier', 'warehouse', 'total_amount']

    def create(self, validated_data):
        supplier_slug = validated_data.pop('supplier_slug')
        warehouse_slug = validated_data.pop('warehouse_slug')
        
        try:
            supplier = Supplier.objects.get(slug=supplier_slug)
        except Supplier.DoesNotExist:
            raise serializers.ValidationError({'supplier_slug': 'Invalid supplier slug.'})
        
        try:
            warehouse = Warehouse.objects.get(slug=warehouse_slug)
        except Warehouse.DoesNotExist:
            raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})
        
        validated_data['supplier'] = supplier
        validated_data['warehouse'] = warehouse
        return super().create(validated_data)

    def update(self, instance, validated_data):
        supplier_slug = validated_data.pop('supplier_slug', None)
        warehouse_slug = validated_data.pop('warehouse_slug', None)

        if supplier_slug:
            try:
                instance.supplier = Supplier.objects.get(slug=supplier_slug)
            except Supplier.DoesNotExist:
                raise serializers.ValidationError({'supplier_slug': 'Invalid supplier slug.'})

        if warehouse_slug:
            try:
                instance.warehouse = Warehouse.objects.get(slug=warehouse_slug)
            except Warehouse.DoesNotExist:
                raise serializers.ValidationError({'warehouse_slug': 'Invalid warehouse slug.'})

        return super().update(instance, validated_data)


# ---------------- PurchaseOrderItem ----------------
class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_slug = serializers.SlugField(write_only=True)
    variant_slug = serializers.SlugField(write_only=True, required=False, allow_null=True)
    purchase_order_slug = serializers.SlugField(write_only=True)
    
    product = serializers.SerializerMethodField(read_only=True)
    variant = serializers.SerializerMethodField(read_only=True)
    purchase_order = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'purchase_order', 'purchase_order_slug', 
            'product', 'product_slug', 'variant', 'variant_slug', 
            'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['id', 'purchase_order', 'product', 'variant', 'total_price']

    def get_product(self, obj):
        return {'id': obj.product.id, 'name': obj.product.name, 'slug': obj.product.slug} if obj.product else None

    def get_variant(self, obj):
        return {'id': obj.variant.id, 'sku': obj.variant.sku, 'slug': obj.variant.slug} if obj.variant else None

    def get_purchase_order(self, obj):
        return {'id': obj.purchase_order.id, 'order_number': obj.purchase_order.order_number, 'slug': obj.purchase_order.slug} if obj.purchase_order else None

    def create(self, validated_data):
        product_slug = validated_data.pop('product_slug')
        variant_slug = validated_data.pop('variant_slug', None)
        purchase_order_slug = validated_data.pop('purchase_order_slug')

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})
        
        variant = None
        if variant_slug:
            try:
                variant = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})
        
        try:
            purchase_order = PurchaseOrder.objects.get(slug=purchase_order_slug)
        except PurchaseOrder.DoesNotExist:
            raise serializers.ValidationError({'purchase_order_slug': 'Invalid purchase order slug.'})

        validated_data['product'] = product
        validated_data['variant'] = variant
        validated_data['purchase_order'] = purchase_order
        return super().create(validated_data)

    def update(self, instance, validated_data):
        product_slug = validated_data.pop('product_slug', None)
        variant_slug = validated_data.pop('variant_slug', None)
        purchase_order_slug = validated_data.pop('purchase_order_slug', None)

        if product_slug:
            try:
                instance.product = Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_slug': 'Invalid product slug.'})

        if variant_slug:
            try:
                instance.variant = Variant.objects.get(slug=variant_slug)
            except Variant.DoesNotExist:
                raise serializers.ValidationError({'variant_slug': 'Invalid variant slug.'})

        if purchase_order_slug:
            try:
                instance.purchase_order = PurchaseOrder.objects.get(slug=purchase_order_slug)
            except PurchaseOrder.DoesNotExist:
                raise serializers.ValidationError({'purchase_order_slug': 'Invalid purchase order slug.'})

        return super().update(instance, validated_data)
    
    
# ---------------- GoodsReceipt ----------------
class GoodsReceiptSerializer(serializers.ModelSerializer):
    purchase_order_id = serializers.UUIDField(write_only=True)
    purchase_order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = [
            "id",
            "slug",
            "purchase_order",
            "purchase_order_id",
            "receipt_date",
            "status",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate(self, data):
        """Custom validations for business rules"""
        purchase_order_id = data.get("purchase_order_id")
        if purchase_order_id:
            try:
                PurchaseOrder.objects.get(id=purchase_order_id)
            except PurchaseOrder.DoesNotExist:
                raise serializers.ValidationError(
                    {"purchase_order_id": "Invalid purchase order ID."}
                )
        return data

    def create(self, validated_data):
        po_id = validated_data.pop("purchase_order_id")
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        validated_data["purchase_order"] = purchase_order
        return super().create(validated_data)

    def update(self, instance, validated_data):
        po_id = validated_data.pop("purchase_order_id", None)
        if po_id:
            try:
                purchase_order = PurchaseOrder.objects.get(id=po_id)
                validated_data["purchase_order"] = purchase_order
            except PurchaseOrder.DoesNotExist:
                raise serializers.ValidationError(
                    {"purchase_order_id": "Invalid purchase order ID."}
                )
        return super().update(instance, validated_data)
