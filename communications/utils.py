from django.core.mail import send_mail
from django.conf import settings
from .models import EmailLog

def simulate_email(to_email, subject, message):
    """
    Sends an email and creates a log entry in the database.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        email_log = EmailLog.objects.create(
            to_email=to_email,
            subject=subject,
            message=message,
            status='sent'
        )
        print(f" [EMAIL SENT] To: {to_email} | Subject: {subject}")
        return email_log
    except Exception as e:
        print(f"Error sending email and creating log: {e}")
        email_log = EmailLog.objects.create(
            to_email=to_email,
            subject=subject,
            message=message,
            status='failed'
        )
        return None
