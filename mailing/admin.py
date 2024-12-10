from django.contrib import admin

from .models import Mailing, Message, Recipient

admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(Mailing)


class MailingAdmin(admin.ModelAdmin):
    list_display = ("message", "status", "is_active")
    list_editable = ("is_active",)
