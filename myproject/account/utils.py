from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from account.models import ServiceUse, UserProfile


def get_number_of_hits(user):
    """Get the number of times this user has hit the Thai API."""

    return ServiceUse.objects.get(user=user).number_of_hits


def update_number_of_hits(user, number_of_hits):
    """Update the number of times this user has hit the Thai API."""

    service_use = ServiceUse.objects.get(user=user)
    service_use.number_of_hits = number_of_hits
    service_use.save()

    print(ServiceUse.objects.get(user=user).number_of_hits)
    if int(ServiceUse.objects.get(user=user).number_of_hits) == 10:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.credit_balance >= 1:
            current_balance = user_profile.credit_balance
            current_balance -= 1
            user_profile.credit_balance = current_balance
            user_profile.save()
        elif user_profile.has_subscribed == 2:
            print("Payment Email send")


def check_user_has_credit_or_subscription(user):
    """
    Checks if a user has either a credit balance greater than or equal to 1 or has
    subscribed.
    """

    user_profile = UserProfile.objects.get(user=user)
    if user_profile.credit_balance < 1 and user_profile.has_subscribed == 1:
        return True
    return False


def send_verification_email(request, user, mail_subject, email_template):
    current_site = get_current_site(request)
    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.content_subtype = "html"
    mail.send()
