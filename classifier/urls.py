from django.urls import path
from .views import PredictApiView,RegisterView,LoginApiView   
from . import views

urlpatterns=[
    path("predict/",PredictApiView.as_view(),name="predict"),
    path("register/",RegisterView.as_view(),name="register_api"),
    path("login/",LoginApiView.as_view(),name="login_api")

]           