# src/web/website/utils/email_utils.py
from django.core.mail import send_mail

def send_detection_success_email(user_email):
    subject = "Detection Successful"
    message = "Hi! Your image has been successfully detected. Thank you for using our service."
    from_email = None  # Uses DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
