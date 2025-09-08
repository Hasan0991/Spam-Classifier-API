from django.shortcuts import render
from django.http import HttpResponse
from .serializer import PredictSerializer
from .ml_model import predict 
from rest_framework import status
from rest_framework.views import APIView


class PredictView(APIView):
    def post(self,request):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            text=serializer.validated_data["text"]
            prediction = predict(text)
            return HttpResponse(f"Prediction is:{prediction}")
        return HttpResponse("GET THE FUCK OUT")
