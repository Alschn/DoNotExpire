from django.contrib import admin

from manager.models import Account
from .models import Profile


class AccountsInline(admin.TabularInline):
    model = Account


class ProfilesAdmin(admin.ModelAdmin):
    list_select_related = ('user',)
    inlines = (
        AccountsInline,
    )


admin.site.register(Profile, ProfilesAdmin)
