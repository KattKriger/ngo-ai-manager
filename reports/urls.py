
from django.urls import path
from .views import report_list, create_report

urlpatterns = [
    path('', report_list, name='report_list'),
    path('create/', create_report, name='create_report'),
]  
