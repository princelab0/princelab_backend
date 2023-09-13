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
    if user_profile.credit_balance < 1 and user_profile.has_subscribed == "Basic":
        return True
    return False
