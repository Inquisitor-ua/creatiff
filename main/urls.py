from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #Hello world
    path('homepage/', views.homepage, name='homepage'),
    path('process_contact_form/', views.process_contact_form, name='process_contact_form')
]