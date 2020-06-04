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
