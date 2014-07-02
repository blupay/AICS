from models import Position
from models import Voyage
from models import Cargo
from model_report.widgets import RangeField, RangeWidget
from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)
from django.utils.translation import ugettext_lazy as _

class Position_Report(ReportAdmin):
	title=('Position Report')
	model= Position
	fields = ['VOYAGE','SP','TYPE','DATE_RE','TIME_RE','LATITUDE','LONGITUDE','ORIGIN_PORT','DESTINATION','ETA_DATE','ETA_TIME','ETA_LOCALTIME','DIST_DIALY','DIST_VOYAGE','DIST_REMAINING','DIST_PORT','HOURS_DAILY','HOURS_VOYAGE','HOURS_MAN','HOURS_PORT','SPEED_DAILY','SPEED_VOYAGE','ROB_IFO','ROB_MGO','ROB_FW','ROB_BALLAST','LIFTED_MGO','LIFTED_FW','CONSUMPTION_IFO','CONSUMPTION_MGO','CONSUMPTION_FW']
	list_order_by = ('DATE_RE',)
	list_filter = ('DATE_RE',)
	template_name = ''
	
	type = 'report'
	report_totals = {
	
        
        }
	override_field_formats = {
	
	}





class Container_Report(ReportAdmin):
	title=('Container Breakdown')
	model = Cargo
	fields = ['PORT','VOYAGE.Voyage_name','V_DATE','FD_20DR','FD_20RF','FD_40DR','FD_40RF','FD_45HC','FD_OTHER','FD_TOTAL','MTD_20DR','MTD_20RF','MTD_40DR','MTD_40RF','MTD_45HC','MTD_OTHER','MTD_TOTAL','FL_20DR','FL_20RF','FL_40DR','FL_40RF','FL_45HC','FL_OTHER','FL_TOTAL','MTL_20DR','MTL_20RF','MTL_40DR','MTL_40RF','MTL_45HC','MTL_OTHER','MTL_TOTAL','loaded_total','discharge_total','SUM']
	list_order_by = ('V_DATE',)
	list_filter = ('V_DATE','VOYAGE',)
	template_name = ''

	type = 'report'

	report_totals = {
        'FD_TOTAL': sum_column,
	'MTD_TOTAL': sum_column,
	'FL_TOTAL': sum_column,
	'MTL_TOTAL': sum_column,
	'SUM':sum_column,

        }
	override_field_formats = {
	
	}


	override_field_labels = {
       
       
    	}
	exports = ('excel',)

class Crew_Voyage_Report(ReportAdmin):
	title=('Crew Voyage Report')
	model = Voyage
	fields = ['VOYAGE','LEG','VOYAGE_CREW.crew_name']
	list_filter = ('VOYAGE','LEG')
	type = 'report'
	
	report_totals = {
        
        }
	override_field_formats = {
	
	}
reports.register ('container-report',Container_Report)
reports.register('crew-voyage-report',Crew_Voyage_Report)
reports.register('position-report',Position_Report)
