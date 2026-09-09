from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'national_id', 'phone_number', 'organization_name', 'is_verified_employer', 'created_at']
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(
        choices=(User.Role.EMPLOYER, User.Role.PUBLIC_VERIFIER),
        default=User.Role.PUBLIC_VERIFIER,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'national_id', 'phone_number', 'organization_name']

    def validate(self, attrs):
        candidate_user = User(
            username=attrs.get('username', ''),
            email=attrs.get('email', ''),
            first_name=attrs.get('first_name', ''),
            last_name=attrs.get('last_name', ''),
            role=attrs.get('role', User.Role.PUBLIC_VERIFIER),
            national_id=attrs.get('national_id'),
            phone_number=attrs.get('phone_number'),
            organization_name=attrs.get('organization_name'),
        )
        try:
            validate_password(attrs['password'], user=candidate_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)}) from exc
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.Role.PUBLIC_VERIFIER),
            national_id=validated_data.get('national_id'),
            phone_number=validated_data.get('phone_number'),
            organization_name=validated_data.get('organization_name')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
