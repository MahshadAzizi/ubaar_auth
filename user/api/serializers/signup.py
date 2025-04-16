from rest_framework import serializers

from user.models import User
from user.services.otp_service import OTPService


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'password',
        ]

    def validate(self, attrs):
        phone = attrs.get('phone_number')

        is_verified = OTPService.is_verified(phone_number=phone)
        if not is_verified:
            raise serializers.ValidationError({'otp': 'Phone number is not verified yet.'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
