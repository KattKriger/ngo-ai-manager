from .models import Report
from django.shortcuts import render, redirect
from .forms import ReportForm
from django.db.models import Sum
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl import load_workbook


def report_list(request):

    selected_year = request.GET.get('year')

    reports = Report.objects.all()
    chart_data = (
        Report.objects
        .values('year')
        .annotate(total_attendance=Sum('internal_attendance') + Sum('external_attendance'))
        .order_by('year')
    )
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
        'chart_data': chart_data,
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

def export_excel(request):

    reports = Report.objects.all()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "NGO Reports"
    
    ws.append([
        'Year',
        'Month',
        'Internal Attendance',
        'External Attendance',
        'Deaths'
    ])
    
    for report in reports:
        ws.append([
            report.year,
            report.month,
            report.internal_attendance,
            report.external_attendance,
            report.deaths
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    response['Content-Disposition'] = ('attachment; filename=ngo_reports.xlsx')

    wb.save(response)
    
    return response

def import_excel(request):

    if request.method == 'POST':

        excel_file = request.FILES['excel_file']

        workbook = load_workbook(excel_file)

        sheet = workbook.active
        
        for row in sheet.iter_rows(min_row=2, values_only=True):

            year = row[0]
            month = row[1]
            internal_attendance = row[2]
            external_attendance = row[3]
            deaths = row[4]

            Report.objects.create(
                year=year,
                month=month,
                internal_attendance=internal_attendance,
                external_attendance=external_attendance,
                deaths=deaths
            )
        
        return redirect('/')
    
    return render(request, 'reports/import_excel.html')