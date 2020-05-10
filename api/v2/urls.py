from django.urls import path
from . import views

urlpatterns = [
    path('find/', views.FindView.as_view(), name='find')
]
