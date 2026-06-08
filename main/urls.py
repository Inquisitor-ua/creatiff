from django.urls import path
from . import views

urlpatterns = [
    path('process_contact_form/', views.ProcessContactFormView.as_view(), name='process_contact_form'),
]