from celery import shared_task
import time


@shared_task
def send_sms_task(phone_number, code):
    print(f"[SMS] Sending OTP '{code}' to {phone_number}")
    time.sleep(2)
    print(f'[SMS] Sent successfully.')
