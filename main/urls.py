from django.urls import path
from . import views

urlpatterns = [
    path('process_contact_form/', views.process_contact_form, name='process_contact_form'),
]