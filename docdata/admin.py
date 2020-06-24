from django.contrib import admin
from . models import RawData, ProcessedData, BillItem

class RawDataAdmin(admin.ModelAdmin):
    list_display= ('source_file', 'date_created', 'time_created', 'json_data', 'device_transfer')

class ProcessedDataAdmin(admin.ModelAdmin):
    list_display= ('rawdata', 'invoice_id', 'order_id', 'customer_id', 'date_issue', 'amount_total', 'amount_due', 'sender_name', 'sender_address', 'sender_vat_id', 'recipient_name', 'recipient_address', 'all_items')

class BillItemAdmin(admin.ModelAdmin):
    list_display= ('rawdata', 'item_name', 'item_quantity', 'item_total_amount')

# Register your models here.
admin.site.register(RawData, RawDataAdmin)
admin.site.register(ProcessedData, ProcessedDataAdmin)
admin.site.register(BillItem, BillItemAdmin)

# Admin Action Functions
def ProcessRawData(modeladmin, request, queryset):
    for object in queryset:
        res_dict = object.json_data
        if (ProcessedData.objects.filter(rawdata=object).exists()):
            items, dict_base = "", res_dict['results'][0]['content']
            for each in dict_base[5]['children'][0]['children']:
                items+=each['children'][0]['value'].replace("\n"," ")+", "
            ProcessedData.objects.filter(rawdata=object).update(
                rawdata = object,
                invoice_id = dict_base[0]['children'][0]['value'],
                order_id = dict_base[0]['children'][1]['value'],
                customer_id = dict_base[0]['children'][2]['value'],
                date_issue = dict_base[0]['children'][3]['value'],
                amount_total = dict_base[1]['children'][2]['value'],
                amount_due = dict_base[1]['children'][3]['value'],
                sender_name = dict_base[2]['children'][0]['value'],
                sender_address = dict_base[2]['children'][1]['value'],
                sender_vat_id = dict_base[2]['children'][3]['value'],
                recipient_name = dict_base[2]['children'][4]['value'],
                recipient_address = dict_base[2]['children'][5]['value'],
                all_items = items,
                )
            if(BillItem.objects.filter(rawdata = object).exists()):
                pass
            else:
                for each in dict_base[5]['children'][0]['children']:
                    items+=each['children'][0]['value'].replace("\n"," ")
                    BillItem.objects.create(rawdata= object, item_name=each['children'][0]['value'].replace("\n"," ") , item_quantity= each['children'][1]['value'], item_total_amount=each['children'][4]['value'])
        else:
            items, dict_base = "", res_dict['results'][0]['content']
            for each in dict_base[5]['children'][0]['children']:
                items+=each['children'][0]['value'].replace("\n"," ")+", "
            ProcessedData.objects.create(
                rawdata = object,
                invoice_id = dict_base[0]['children'][0]['value'],
                order_id = dict_base[0]['children'][1]['value'],
                customer_id = dict_base[0]['children'][2]['value'],
                date_issue = dict_base[0]['children'][3]['value'],
                amount_total = dict_base[1]['children'][2]['value'],
                amount_due = dict_base[1]['children'][3]['value'],
                sender_name = dict_base[2]['children'][0]['value'],
                sender_address = dict_base[2]['children'][1]['value'],
                sender_vat_id = dict_base[2]['children'][3]['value'],
                recipient_name = dict_base[2]['children'][4]['value'],
                recipient_address = dict_base[2]['children'][5]['value'],
                all_items = items,
                )
            if(BillItem.objects.filter(rawdata = object).exists()):
                pass
            else:
                for each in dict_base[5]['children'][0]['children']:
                    items+=each['children'][0]['value'].replace("\n"," ")
                    BillItem.objects.create(rawdata= object, item_name=each['children'][0]['value'].replace("\n"," ") , item_quantity= each['children'][1]['value'], item_total_amount=each['children'][4]['value'])

admin.site.add_action(ProcessRawData, "Process Selected RawData")