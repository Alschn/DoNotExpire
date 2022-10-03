from django.contrib import admin
from .models import Profile
from manager.models import Account


class AccountsInline(admin.TabularInline):
    model = Account


class ProfilesAdmin(admin.ModelAdmin):
    inlines = [
        AccountsInline,
    ]


admin.site.register(Profile, ProfilesAdmin)
