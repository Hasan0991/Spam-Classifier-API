from django.urls import path
from .views import PredictView,RegisterView
from . import views

urlpatterns=[
    path("predict/",PredictView.as_view(),name="predict"),
    path("register/",RegisterView.as_view(),name="register")
]           