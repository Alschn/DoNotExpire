from django.contrib import admin
from .models import Account, Character


class CharsInline(admin.TabularInline):
    model = Character

class AccountAdmin(admin.ModelAdmin):
    inlines = [
        CharsInline,
    ]

admin.site.register(Character)
admin.site.register(Account, AccountAdmin)
