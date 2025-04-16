from django.http import JsonResponse
from user.services.throttle_service import ThrottleService


class ThrottleBlockMiddleware:
    """
    Middleware to check if a request should be blocked due to too many failed attempts
    for OTP send, OTP verify, and login endpoints.
    """

    THROTTLE_PATHS = {
        "/api/v1/users/send-otp/": "otp_send",
        "/api/v1/users/verify-otp/": "otp_verify",
        "/api/v1/users/signup/": "otp_verify",
        "/api/v1/users/login/": "login",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        method = request.method

        scope = self.THROTTLE_PATHS.get(path)
        if scope and method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            phone = request.POST.get("phone_number") or request.GET.get("phone_number")

            if ThrottleService.is_blocked(scope, ip, phone):
                return JsonResponse(
                    {"detail": f"Too many failed attempts on '{scope}'. Try again later."},
                    status=429
                )

        return self.get_response(request)
