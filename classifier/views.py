from django.shortcuts import render
from rest_framework.response import Response
from .serializer import PredictSerializer,RegisterSerializer
from .ml_model import predict 
from rest_framework import status
from rest_framework.views import APIView,View
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def myapp(request):
    return render(request,"register.html") 

class PredictView(APIView):
    permission_classes=[IsAuthenticated]
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
            return  redirect('login_page')  
        return render(request, 'register.html', {'errors': serializer.errors})
    
class LoginView(APIView):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('main_page')
        return render(request,'login.html', {"error": "Invalid username or password"})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    
    
@method_decorator(login_required(login_url='/login/'), name="dispatch")
class DashboardView(View):
    def get(self, request):
        return render(request, "main.html", {"user": request.user})