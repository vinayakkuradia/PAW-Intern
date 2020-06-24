from rest_framework import serializers
from . models import RawData, ProcessedData, BillItem

class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = '__all__'

class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = '__all__'

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = '__all__'

