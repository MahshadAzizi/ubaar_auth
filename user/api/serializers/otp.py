from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        if not value.startswith('+98') and not value.startswith('09'):
            raise serializers.ValidationError('Invalid phone number format')
        return value
