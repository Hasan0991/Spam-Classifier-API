from django.shortcuts import render
from rest_framework.response import Response
from .serializer import PredictSerializer,RegisterSerializer
from .ml_model import predict 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect


def myapp(request):
    return render(request,"register.html") 

def login_page(request):
    return render(request,'login.html')
class PredictView(APIView):
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
            serializer.save()
            return render(request,'login.html', {'success': 'User registered successfully'})
        return render(request, 'register.html', {'errors': serializer.errors})
    
class LoginView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
