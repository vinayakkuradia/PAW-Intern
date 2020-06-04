from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import RawData
from . serializers import RawDataSerializer


class RawDataDisplay(APIView):

    def get(selfself, request):
        RawData1 = RawData.objects.all()
        serializer = RawDataSerializer(RawData1, many=True)
        return Response(serializer.data)

    def post(self):
        pass
