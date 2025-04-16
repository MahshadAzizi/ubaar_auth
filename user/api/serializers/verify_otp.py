from rest_framework import serializers
from user.services.otp_service import OTPService


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        code = attrs.get('code')

        is_valid, message = OTPService.verify_otp(phone, code)
        if not is_valid:
            raise serializers.ValidationError({'otp': message})
        return attrs
