from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.serializers import SendOTPSerializer
from user.services.otp_service import OTPService


class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')

        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            OTPService.create_otp(phone)
            return Response(
                {'detail': 'OTP sent successfully.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
