from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings
from communications.models import EmailLog # Import EmailLog for logging

@receiver(social_account_added)
def user_signed_up_with_google(request, socialaccount, **kwargs):
    user = socialaccount.user
    subject = "Welcome to West Africa Decor Tiles!"
    message = f"Dear {user.username},\n\nWelcome to West Africa Decor Tiles! We're excited to have you on board.\n\nBest regards,\nYour West Africa Decor Tiles Team"
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        EmailLog.objects.create(
            to_email=user.email,
            subject=subject,
            message=message,
            status='sent'
        )
        print(f" [EMAIL SENT] Welcome email to {user.email}")
    except Exception as e:
        print(f"Error sending welcome email to {user.email}: {e}")
        EmailLog.objects.create(
            to_email=user.email,
            subject=subject,
            message=message,
            status='failed'
        )

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Send an email to the user when they log in.
    """
    subject = 'Successful Login to Your Account'
    message = f'Dear {user.username},\n\nThis is a notification that your account was just accessed. If this was not you, please contact us immediately.\n\nBest regards,\nYour West Africa Decor Tiles Team'
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        EmailLog.objects.create(
            to_email=user.email,
            subject=subject,
            message=message,
            status='sent'
        )
        print(f" [EMAIL SENT] Login alert to {user.email}")
    except Exception as e:
        print(f"Error sending login alert email to {user.email}: {e}")
        EmailLog.objects.create(
            to_email=user.email,
            subject=subject,
            message=message,
            status='failed'
        )