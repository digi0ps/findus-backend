from django.urls import path, include
from . import views

urlpatterns = [
    path('gallery/', views.PhotoView.as_view(), name='gallery'),
    path('person/', views.PersonView.as_view(), name='person'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('v2/', include('api.v2.urls')),
]
