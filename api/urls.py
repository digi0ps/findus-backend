from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.PhotoView.as_view(), name='gallery'),
]
