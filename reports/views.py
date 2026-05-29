from django.shortcuts import render

from django.shortcuts import render
from .models import Report

def report_list(request):

    selected_year = request.GET.get('year')

    reports = Report.objects.all()

        if selected_year:
            reports = reports.filter(year=selected_year)
        
        years = Report.objects.values_list('year', flat=True).distinct().order_by('year')

    return render(request, 'reports/report_list.html', {
        'reports': reports,
        'years': years
        'selected_year': selected_year
        })