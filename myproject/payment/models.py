from django.db import models

from account.models import User

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_name = models.CharField(max_length=100, null=True, blank=True)
    payment_amount = models.FloatField(null=True, blank=True)
    unique_payment_id = models.TextField(max_length=500, null=True, blank=True)
    unique_id_for_user = models.TextField(max_length=500, null=True, blank=True)
    payment_status = models.BooleanField(default=False, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "{self.user.email} - {self.pament_amount} - {self.payment_status}"
