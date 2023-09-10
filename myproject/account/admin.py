from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User, ServiceUse, Transition

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "balance", "is_active")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class TransitionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "transition_date")
    ordering = ("-transition_date",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ServiceUseAdmin(admin.ModelAdmin):
    list_display = ("user", "number_of_hits", "last_hit")
    ordering = ("-last_hit",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(ServiceUse, ServiceUseAdmin)
admin.site.register(Transition, TransitionAdmin)
