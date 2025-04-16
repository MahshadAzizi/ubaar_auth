from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.api.serializers import LoginSerializer
from user.services.throttle_service import ThrottleService


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')
        phone = request.data.get('phone_number')

        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            ThrottleService.increment('login', ip, phone)
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        ThrottleService.reset('login', ip, phone)

        return Response({
            'results': serializer.validated_data,
            'status': status.HTTP_200_OK
        })
