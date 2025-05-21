from rest_framework import serializers
from django.contrib.auth import get_user_model

from orders.models import Address

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['full_address']


class UserSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone = serializers.CharField()
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("رمز عبور وارد شده یکسان نیست!")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(phone=validated_data['phone'], fullname=validated_data['fullname'])
        user.set_password(validated_data['password1'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'fullname']
