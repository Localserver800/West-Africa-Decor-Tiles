from django.contrib import admin
from .models import EmailLog

class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['to_email', 'subject', 'sent_at', 'status']
    list_filter = ['status', 'sent_at']
    readonly_fields = ['sent_at']

admin.site.register(EmailLog, EmailLogAdmin)