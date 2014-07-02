from models import Crew_detail
from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)


class Crew_Details_Report(ReportAdmin):
	title=('All Crew Details')
	model= Crew_detail
	fields = ['surname','othernames','sex','date_Of_birth','Nationality','rank__rank','no_of_identity','ship__ship_name','email']
	#list_order_by = ('surname',)
	list_group_by = ('rank__rank','sex','ship__ship_name',)
	list_serie_fields = ('rank__rank','ship__ship_name',)

	type = 'chart'

	group_totals = {
        'speciality': count_column,
	
	}

	chart_types = ('pie', 'column', 'line')

reports.register('all-Crew-report',Crew_Details_Report)





class Ship_Crew_Details_Report(ReportAdmin):
	title=('Ship Crew Details')
	model= Crew_detail
	fields = ['surname','othernames','sex','date_Of_birth','Nationality','rank__rank','no_of_identity','ship__ship_name']
	list_order_by = ('surname',)
	list_filter = ('ship__ship_name','rank__rank',)
	list_serie_fields = ('ship__ship_name','rank__rank',)
	type = 'report'
	report_totals = {
        
        }

reports.register('Ship-Crew-Report',Ship_Crew_Details_Report)
