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
from django.views.decorators.csrf  import csrf_exempt
from django.utils.decorators import method_decorator


def myapp(request):
    return render(request,"register.html") 

@method_decorator(login_required(login_url='/login/'),name="dispatch")
class PredictPageView(View):
    def get(self,request):
        return render(request,'predict.html')
    
    def post(self,request):
        serializer = PredictSerializer(data={'text':request.POST.get("text")})
        if serializer.is_valid():
            text=serializer.validated_data["text"]
            accuracy_number,prediction = predict(text)
            return render(request, 'predict.html', {
                'prediction': prediction,
                'probability': accuracy_number,
                'text': text
            })
        return render(request, 'predict.html', {'errors': serializer.errors})

class PredictApiView(APIView):
    def post(self,request):
        serializer = PredictSerializer(data={'text':request.data.get("text")})
        if serializer.is_valid():
            text=serializer.validated_data["text"]
            accuracy_number,prediction = predict(text)
            return render(request, 'predict.html', {
                'prediction': prediction,
                'probability': accuracy_number,
                'text': text
            })
        return  Response({"error":serializer.errors},status=401)
    
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  redirect('login_page')  
        return render(request, 'register.html', {'errors': serializer.errors})
    
class LoginPageView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('prediction_page')
        return render(request,'login.html', {'errors': "Invalid username or password"})

class LoginApiView(APIView):
    
    def post(self,request):
        username = request.data.get("username")  
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)    
            return redirect("prediction_page")
        return Response({"errors":"invalid credentials"})
    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    
    
@method_decorator(login_required(login_url='/login/'), name="dispatch")
class DashboardView(View):
    def get(self, request):
        return render(request, "main.html", {"user": request.user})