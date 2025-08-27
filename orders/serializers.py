from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Payment, Refund, Invoice
from catalog.models import Product, Variant


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    variant_name = serializers.CharField(source="variant.name", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id", "slug", "cart", "product", "product_name", "variant", "variant_name",
            "quantity", "price", "total_price", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "total_price", "created_at", "updated_at"]

    def validate(self, data):
        """Ensure quantity is positive and product exists"""
        if data.get("quantity", 0) <= 0:
            raise serializers.ValidationError({"quantity": "Quantity must be greater than 0."})

        if not Product.objects.filter(id=data.get("product").id).exists():
            raise serializers.ValidationError({"product": "Invalid product."})

        if data.get("variant") and not Variant.objects.filter(id=data["variant"].id, product=data["product"]).exists():
            raise serializers.ValidationError({"variant": "Variant does not belong to the selected product."})

        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id", "slug", "user", "session_key", "is_active",
            "items", "total_items", "total_price", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.items.all())


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id", "slug", "order", "product", "product_name",
            "quantity", "price", "subtotal", "created_at"
        ]
        read_only_fields = ["id", "slug", "subtotal", "created_at"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "slug", "user", "user_email", "status",
            "total_amount", "discount_amount", "final_amount",
            "shipping_address", "billing_address",
            "payment_status", "payment_method",
            "tracking_number", "notes",
            "items", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate(self, data):
        if data.get("final_amount", 0) < 0:
            raise serializers.ValidationError({"final_amount": "Final amount cannot be negative."})
        return data


class PaymentSerializer(serializers.ModelSerializer):
    order_slug = serializers.CharField(source="order.slug", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id", "slug", "order", "order_slug", "user", "user_email",
            "amount", "currency", "method", "status", "transaction_id",
            "payment_gateway_response", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be greater than 0.")
        return value


class RefundSerializer(serializers.ModelSerializer):
    payment_slug = serializers.CharField(source="payment.slug", read_only=True)

    class Meta:
        model = Refund
        fields = [
            "id", "slug", "payment", "payment_slug",
            "amount", "reason", "status", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than 0.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    order_slug = serializers.CharField(source="order.slug", read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id", "slug", "order", "order_slug", "invoice_number",
            "amount", "issued_date", "due_date", "created_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "issued_date"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invoice amount must be greater than 0.")
        return value
