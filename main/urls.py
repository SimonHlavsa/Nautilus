from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contacts/', views.contacts, name='contacts'),
    path('registration/', views.registration, name='registration'),
    path('calendar/', views.calendar, name='calendar'),
    path('gallery/', views.gallery, name='gallery'),
]
