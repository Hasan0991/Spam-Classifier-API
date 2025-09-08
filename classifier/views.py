from django.shortcuts import render
from rest_framework.response import Response
from .serializer import PredictSerializer
from .ml_model import predict 
from rest_framework import status
from rest_framework.views import APIView


class PredictView(APIView):
    def post(self,request):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            text=serializer.validated_data["text"]
            accuracy_number,prediction = predict(text)
            return Response({'prediction':prediction,
                             'probability':accuracy_number}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
