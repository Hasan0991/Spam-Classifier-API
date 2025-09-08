from django.shortcuts import render
from rest_framework.response import Response
from .serializer import PredictSerializer,RegisterSerializer
from .ml_model import predict 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated

class PredictView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self,request):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            text=serializer.validated_data["text"]
            accuracy_number,prediction = predict(text)
            return Response({'prediction':prediction,
                             'probability':accuracy_number}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user =serializer.save()
            return Response({"message":"User registered successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)