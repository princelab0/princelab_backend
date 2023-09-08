from django.contrib import admin
from core.models import User

# Register your models here.
admin.site.register([User])
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']