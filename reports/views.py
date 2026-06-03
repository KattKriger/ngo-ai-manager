from .models import Report
from django.shortcuts import render, redirect
from .forms import ReportForm
from django.db.models import Sum


def report_list(request):

    selected_year = request.GET.get('year')

    reports = Report.objects.all()
    total_reports = reports.count()
    total_internal_attendance = reports.aggregate(
        Sum('internal_attendance')
        )['internal_attendance__sum']
    total_external_attendance = reports.aggregate(
        Sum('external_attendance')
        )['external_attendance__sum']
    total_deaths = reports.aggregate(
        Sum('deaths')
        )['deaths__sum']

    if selected_year:
            reports = reports.filter(year=selected_year)
        
    years = Report.objects.values_list(
        'year',
        flat=True
    ).distinct().order_by('year')

    return render(request, 'reports/report_list.html', {
        'reports': reports,
        'years': years,
        'selected_year': selected_year,
        'total_reports': total_reports,
        'total_internal_attendance': total_internal_attendance,
        'total_external_attendance': total_external_attendance,
        'total_deaths': total_deaths,
    })

def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ReportForm()
    return render(
        request,
        'reports/create_report.html',
        {'form': form}
    )