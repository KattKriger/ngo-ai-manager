
from django.urls import path
from .views import (
    report_list,
    create_report,
    export_excel,
    import_excel,
    edit_report,
    delete_report
)

urlpatterns = [
    path('', report_list, name='report_list'),
    path('create/', create_report, name='create_report'),
    path('export/', export_excel, name='export_excel'),
    path('import/', import_excel, name='import_excel'),
    path ('edit/<int:report_id>/', edit_report, name='edit_report'),
    path ('delete/<int:report_id>/', delete_report, name='delete_report'),
]  
