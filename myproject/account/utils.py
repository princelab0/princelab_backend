from account.models import ServiceUse


def get_number_of_hits(user):
    """Get the number of times this user has hit the Thai API."""
    return ServiceUse.objects.get(user=user).number_of_hits


def update_number_of_hits(user, number_of_hits):
    """Update the number of times this user has hit the Thai API."""
    service_use = ServiceUse.objects.get(user=user)
    service_use.number_of_hits = number_of_hits
    service_use.save()
