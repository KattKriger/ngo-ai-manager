from .models import Report
from django.shortcuts import render, redirect
from .forms import ReportForm


def report_list(request):

    selected_year = request.GET.get('year')


    selected_year = request.GET.get('year')

    reports = Report.objects.all()

    if selected_year:
            reports = reports.filter(year=selected_year)
        
    years = Report.objects.values_list('year', flat=True).distinct().order_by('year')

    return render(request, 'reports/report_list.html', {
        'reports': reports,
        'years': years,
        'selected_year': selected_year
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