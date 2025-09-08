from django.urls import path
from .views import PredictView
from . import views

urlpatterns=[
    path("predict/",PredictView.as_view())
]           