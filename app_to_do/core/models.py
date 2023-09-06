#importing the models from django.db
from django.db import models

# Create your models here.
class User(models.Model):
    email=models.CharField(max_length=500, verbose_name='email',blank=False,null=True)
    username=models.CharField(max_length=500, verbose_name='Username',blank=False,null=True)
    password=models.CharField(max_length=500,verbose_name='Password',blank=False,null=True)
#declaring the variable with its fieldtype and verbose type. i.e.
#variable=models.FeildType(parameters)

