from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.api.serializers import SignupSerializer
from user.services.throttle_service import ThrottleService


class SignupView(APIView):
    def post(self, request):
        ip = request.META.get('REMOTE_ADDR')
        phone = request.data.get('phone_number')

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            _ = serializer.save()
            ThrottleService.reset('otp_verify', ip, phone)

            return Response({
                'message': 'Signup successful.',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
