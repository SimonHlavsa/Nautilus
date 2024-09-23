from django.urls import path
from django.views.i18n import set_language
from . import views

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path('', views.homepage, name='homepage'),
    path('contacts/', views.contacts, name='contacts'),
    path('registration/', views.registration, name='registration'),
    path('calendar/', views.calendar, name='calendar'),
    path('gallery/', views.gallery, name='gallery'),
]
