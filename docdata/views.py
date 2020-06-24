#from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse
#from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework import status
from . models import RawData, ProcessedData, BillItem
from . serializers import RawDataSerializer, ProcessedDataSerializer, BillItemSerializer


class RawDataDisplay(APIView):

    def get(selfself, request):
        RawData1 = RawData.objects.all()
        serializer = RawDataSerializer(RawData1, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class ProcessedDataDisplay(APIView):

    def get(selfself, request):
        ProcessedData1 = ProcessedData.objects.all()
        serializer = ProcessedDataSerializer(ProcessedData1, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class BillItemDisplay(APIView):

    def get(selfself, request):
        BillItem1 = BillItem.objects.all()
        serializer = BillItemSerializer(BillItem1, many=True)
        return Response(serializer.data)

    def post(self):
        pass