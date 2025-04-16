from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.api.serializers import VerifyOTPSerializer
from user.services.throttle_service import ThrottleService


class VerifyOTPView(APIView):
    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        phone = request.data.get('phone_number')

        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            ThrottleService.reset('otp_verify', ip, phone)
            return Response(
                {'detail': 'OTP verified successfully'},
                status=status.HTTP_200_OK
            )

        ThrottleService.increment('otp_verify', ip, phone)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
