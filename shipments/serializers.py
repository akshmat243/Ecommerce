import re
from rest_framework import serializers
from .models import ShippingMethod, Shipment, ShippingAddress


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = "__all__"

    def validate_base_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Base cost cannot be negative.")
        return value

    def validate_additional_cost_per_kg(self, value):
        if value < 0:
            raise serializers.ValidationError("Additional cost per kg cannot be negative.")
        return value


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"

    def validate_postal_code(self, value):
        if not re.match(r"^[0-9A-Za-z\- ]+$", value):
            raise serializers.ValidationError("Postal code contains invalid characters.")
        return value

    def validate_phone_number(self, value):
        if not re.match(r"^\+?[0-9\- ]{7,15}$", value):
            raise serializers.ValidationError("Invalid phone number format.")
        return value

    def validate(self, data):
        # Only one default shipping address per user
        if data.get("is_default"):
            qs = ShippingAddress.objects.filter(user=data["user"], is_default=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("User already has a default shipping address.")
        return data


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"
        ref_name = "ShipmentsAppShipment" 

    def validate(self, data):
        if data.get("status") == "delivered" and not data.get("delivered_at"):
            raise serializers.ValidationError("Delivered date must be provided when status is 'delivered'.")
        return data
