from django.contrib import admin
from django.db.models import QuerySet

from .models import Account, Character, Equipment


class CharsInline(admin.TabularInline):
    model = Character


class ItemsInline(admin.StackedInline):
    model = Equipment


class CharAdmin(admin.ModelAdmin):
    list_display = ('name', 'char_class', 'level', 'acc')
    list_select_related = ('acc',)
    inlines = (
        ItemsInline,
    )


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'realm', 'last_visited', 'expired')
    list_select_related = ('profile',)
    inlines = (
        CharsInline,
    )


class EquipmentAdmin(admin.ModelAdmin):
    list_select_related = ('char',)


admin.site.register(Character, CharAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Account, AccountAdmin)
