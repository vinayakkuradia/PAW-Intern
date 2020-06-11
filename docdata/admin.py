from django.contrib import admin
from . models import RawData, ProcessedData

class RawDataAdmin(admin.ModelAdmin):
    list_display= ('source_file', 'date_created', 'time_created', 'json_data')

class ProcessedDataAdmin(admin.ModelAdmin):
    list_display= ('rawdata', 'invoice_id', 'order_id', 'customer_id', 'date_issue', 'amount_total', 'amount_due', 'sender_name', 'sender_address', 'sender_vat_id', 'recipient_name', 'recipient_address', 'item_description')

# Register your models here.
admin.site.register(RawData, RawDataAdmin)
admin.site.register(ProcessedData, ProcessedDataAdmin)