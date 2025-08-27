from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User, UserRole, UserProfile, Address
from MBP.models import Role

from MBP.serializers import RoleSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="slug", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "slug",
            "user",
            "age",
            "gender",
            "country",
            "profile_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        if not user:
            raise serializers.ValidationError({"user": "User must be authenticated to create a profile."})

        # Create profile linked to logged-in user
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(read_only=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['slug', 'email', 'full_name', 'password', 'is_active', 'profile', 'roles']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True  # Users can log in immediately after registration
        user.save()

        # Assign default role "customer"
        customer_role, created = Role.objects.get_or_create(
            slug="customer",
            defaults={"name": "Customer"}
        )
        UserRole.objects.create(user=user, role=customer_role)

        return user
    def get_roles(self, obj):
        try:
            user_role = UserRole.objects.get(user=obj)
            return RoleSerializer(user_role.role).data
        except UserRole.DoesNotExist:
            return None
        

class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='slug', queryset=User.objects.all())
    role = serializers.SlugRelatedField(slug_field='slug', queryset=Role.objects.all())
    assigned_by = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'assigned_at', 'assigned_by']
        read_only_fields = ['id', 'assigned_at', 'assigned_by']

    def validate(self, data):
        # Check if user already has a role
        if UserRole.objects.filter(user=data['user']).exists():
            raise serializers.ValidationError({
                'user': 'This user already has a role assigned.'
            })
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        assigned_by = request.user if request else None

        try:
            user_role = UserRole.objects.create(assigned_by=assigned_by, **validated_data)
            return user_role
        except ValidationError as e:
            raise serializers.ValidationError({'error': str(e)})


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )

    class Meta:
        model = Address
        fields = [
            'id', 'user', 'full_name', 'street_address',
            'city', 'state', 'postal_code', 'country',
            'is_default', 'slug', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']

    def validate(self, data):
        # If user already has a default address and trying to add another
        if data.get("is_default"):
            if Address.objects.filter(user=data["user"], is_default=True).exists():
                raise serializers.ValidationError({
                    "is_default": "User already has a default address."
                })
        return data

    def create(self, validated_data):
        try:
            address = Address.objects.create(**validated_data)
            return address
        except ValidationError as e:
            raise serializers.ValidationError({"error": str(e)})
        
    def update(self, instance, validated_data):
        # If updating to default, unset previous default
        if validated_data.get("is_default") and not instance.is_default:
            Address.objects.filter(user=instance.user, is_default=True).update(is_default=False)
        return super().update(instance, validated_data)
    
    
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'slug', 'addresses', 'password',
            'is_active', 'date_joined', 'created_by'
        ]
        read_only_fields = ['id', 'slug', 'date_joined', 'created_by']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance