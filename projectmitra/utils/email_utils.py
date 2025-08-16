
from django.core.mail import send_mail

def send_custom_email(subject, message, recipient_list, from_email=None):
    from_email = from_email or 'hr@qontrix.com'
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")  # or use logging
        raise
