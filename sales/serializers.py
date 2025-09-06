from rest_framework import serializers
from .models import Customer, SalesOrder, SalesOrderItem, SalesPayment, SalesShipment, SalesInvoice
from catalog.models import Product
from inventory.models import Warehouse


# ------------------ Customer ------------------
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id", "slug", "first_name", "last_name", "email", "phone",
            "address", "city", "country", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate_email(self, value):
        qs = Customer.objects.exclude(id=self.instance.id) if self.instance else Customer.objects.all()
        if qs.filter(email=value).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value


# ------------------ SalesOrderItem ------------------
class SalesOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field="slug")

    class Meta:
        model = SalesOrderItem
        fields = ["id", "order", "product", "quantity", "price", "subtotal"]
        read_only_fields = ["id", "subtotal"]


# ------------------ SalesOrder ------------------
class SalesOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_slug = serializers.SlugField(write_only=True)
    items = SalesOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            "id", "slug", "customer", "customer_slug", "order_date",
            "status", "total_amount", "created_by", "items"
        ]
        read_only_fields = ["id", "slug", "order_date", "total_amount"]

    def create(self, validated_data):
        customer_slug = validated_data.pop("customer_slug")
        try:
            customer = Customer.objects.get(slug=customer_slug)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({"customer_slug": "Invalid customer slug."})
        validated_data["customer"] = customer
        return super().create(validated_data)

    def update(self, instance, validated_data):
        customer_slug = validated_data.pop("customer_slug", None)
        if customer_slug:
            try:
                validated_data["customer"] = Customer.objects.get(slug=customer_slug)
            except Customer.DoesNotExist:
                raise serializers.ValidationError({"customer_slug": "Invalid customer slug."})
        return super().update(instance, validated_data)


# ------------------ Payment ------------------
class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(queryset=SalesOrder.objects.all(), slug_field="slug")

    class Meta:
        model = SalesPayment
        fields = ["id", "slug", "order", "payment_date", "amount", "method", "transaction_id"]
        read_only_fields = ["id", "slug", "payment_date"]


# ------------------ Shipment ------------------
class ShipmentSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(queryset=SalesOrder.objects.all(), slug_field="slug")
    warehouse = serializers.SlugRelatedField(queryset=Warehouse.objects.all(), slug_field="slug")

    class Meta:
        model = SalesShipment
        fields = [
            "id", "order", "warehouse", "tracking_number", "carrier",
            "status", "shipped_date", "delivered_date"
        ]
        read_only_fields = ["id"]
        ref_name = "SalesAppShipment"


# ------------------ Invoice ------------------
class InvoiceSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(queryset=SalesOrder.objects.all(), slug_field="slug")

    class Meta:
        model = SalesInvoice
        fields = ["id", "slug", "order", "invoice_date", "total_amount", "due_date", "is_paid"]
        read_only_fields = ["id", "slug", "invoice_date"]
