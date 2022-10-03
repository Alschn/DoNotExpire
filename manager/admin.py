from django.contrib import admin
from .models import Account, Character, Equipment


class CharsInline(admin.TabularInline):
    model = Character


class ItemsInline(admin.StackedInline):
    model = Equipment


class CharAdmin(admin.ModelAdmin):
    inlines = [
        ItemsInline,
    ]


class AccountAdmin(admin.ModelAdmin):
    inlines = [
        CharsInline,
    ]


admin.site.register(Character, CharAdmin)
admin.site.register(Equipment)
admin.site.register(Account, AccountAdmin)
