import random

from user.models import OTP
from user.tasks import send_sms_task


class OTPService:
    OTP_EXPIRY_MINUTES = 5

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    @classmethod
    def create_otp(cls, phone_number):
        code = cls.generate_code()
        otp = OTP.objects.create(phone_number=phone_number, code=code)
        send_sms_task.delay(phone_number, code)
        return otp

    @staticmethod
    def get_latest_otp(phone_number):
        return OTP.objects.filter(
            phone_number=phone_number
        ).order_by('-created_at').first()

    @staticmethod
    def is_verified(phone_number):
        otp = OTPService.get_latest_otp(phone_number)
        if not otp or not otp.is_verified:
            return False
        return True

    @classmethod
    def verify_otp(cls, phone_number, code):
        otp = cls.get_latest_otp(phone_number)
        if not otp:
            return False, 'No OTP found. Please request a new one.'
        if otp.is_expired:
            return False, 'OTP has expired.'
        if otp.code != code:
            return False, 'Invalid OTP code.'

        otp.is_verified = True
        otp.save()
        return True, 'OTP verified successfully.'
