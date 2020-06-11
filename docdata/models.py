from django.db import models
from django.utils import timezone
timezone.localtime(timezone.now())
import jsonfield

# Create your models here.
class RawData(models.Model):
    source_file = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now)
    time_created = models.TimeField(default=timezone.now)
    json_data = jsonfield.JSONField()

    def __str__(self):
        return self.source_file

class ProcessedData(models.Model):
    rawdata = models.ForeignKey(RawData, blank=True, null=True, on_delete=models.CASCADE)
    invoice_id = models.CharField(null=True, max_length=30)
    order_id = models.CharField(null=True, max_length=20)
    customer_id = models.CharField(null=True, max_length=15)
    date_issue = models.CharField(null=True, max_length=12)
    amount_total = models.FloatField(null=True)
    amount_due = models.FloatField(null=True)
    sender_name = models.CharField(null=True, max_length=30)
    sender_address = models.CharField(null=True, max_length=200)
    sender_vat_id = models.CharField(null=True, max_length=30)
    recipient_name = models.CharField(null=True, max_length=30)
    recipient_address = models.CharField(null=True, max_length=200)
    item_description = models.CharField(null=True, max_length=150)

    def __str__(self):
        return self.invoice_id