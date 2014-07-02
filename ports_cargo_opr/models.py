from django.db import models
from django.contrib import admin
from vessel.models import *
from crew.models import Crew_detail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm,TextInput 
from suit.widgets import SuitDateWidget,LinkedSelect, SuitTimeWidget, SuitSplitDateTimeWidget,HTML5Input,AutosizedTextarea,EnclosedInput
from suit.admin import SortableTabularInline

# Create your models here.
class Port(models.Model):
	PORT = models.CharField(primary_key= True,max_length =50,help_text = " eg. TAKORADI")
	date_added = models.DateTimeField(auto_now_add= True)
	
	def __unicode__ (self):
		return '[%s]' %(self.PORT.upper())
		

class Voyage(models.Model):
	VOYAGE = models.CharField(max_length =10,help_text = " eg. 002")
	LEG = models.CharField('status',choices=(("A","A"),("B","B"),("C","C")),max_length = 2,default=" ")
	VOYAGE_CREW = models.ManyToManyField(Crew_detail,related_name = "crew_voyage",blank=True, null=True)
	V_DATE = models.DateField('Date',blank = True, null = True)
	date_added = models.DateTimeField(auto_now= True)
        date_updated = models.DateTimeField(auto_now_add = True)

	def __unicode__ (self):
		return '%s - %s' %(self.VOYAGE,self.LEG)
	
       
	def Voyage_name(self):
		return '%s - %s' %(self.VOYAGE,self.LEG)

	class Meta:
		verbose_name = "Voyage"
		verbose_name_plural="Voyages"

class Cargo (models.Model):
	PORT = models.ForeignKey(Port,related_name='Port')
	VOYAGE = models.ForeignKey(Voyage,unique=False,related_name='Voyage')
	V_DATE = models.DateField('Date',blank = True, null = True)
	loaded_total = models.PositiveIntegerField('SUM LOADED',blank=True,null =True,default=0)
	discharge_total = models.PositiveIntegerField('SUM DISCHARGED',blank=True,null =True,default=0)
	SUM = models.PositiveIntegerField('CARGO TOTAL',blank=True,null =True,default=0)
	
	#discharge-full

	FD_20DR = models.PositiveIntegerField('D/C FULL 20DR',blank=True,null =True,default=0)
	FD_20RF = models.PositiveIntegerField('D/C FULL 20RF',blank=True,null =True,default=0)
	FD_40DR = models.PositiveIntegerField('D/C FULL 40DR',blank=True,null =True,default=0)
	FD_40RF = models.PositiveIntegerField('D/C FULL 40RF',blank=True,null =True,default=0)
	FD_45HC = models.PositiveIntegerField('D/C FULL 45HC',blank=True,null =True,default=0)
	FD_OTHER = models.PositiveIntegerField('D/C FULL OTHER',blank=True,null =True,default=0)
	FD_TOTAL = models.PositiveIntegerField('D/C FULL TEU',blank=True,null =True,default=0)
	
	#discharge-MT
	MTD_20DR = models.PositiveIntegerField('D/C MT 20DR',blank=True,null =True,default=0)
	MTD_20RF = models.PositiveIntegerField('D/C MT 20RF',blank=True,null =True,default=0)
	MTD_40DR = models.PositiveIntegerField('D/C MT 40DR',blank=True,null =True,default=0)
	MTD_40RF = models.PositiveIntegerField('D/C MT 40RF',blank=True,null =True,default=0)
	MTD_45HC = models.PositiveIntegerField('D/C MT 45HC',blank=True,null =True,default=0)
	MTD_OTHER = models.PositiveIntegerField('D/C MT OTHER',blank=True,null =True,default=0)
	MTD_TOTAL = models.PositiveIntegerField('D/C MT TEU',blank=True,null =True,default=0)
	
	#loaded-FULL
	FL_20DR = models.PositiveIntegerField('20DR',blank=True,null =True,default=0)
	FL_20RF = models.PositiveIntegerField('20RF',blank=True,null =True,default=0)
	FL_40DR = models.PositiveIntegerField('40DR',blank=True,null =True,default=0)
	FL_40RF = models.PositiveIntegerField('40RF',blank=True,null =True,default=0)
	FL_45HC = models.PositiveIntegerField('45HC',blank=True,null =True,default=0)
	FL_OTHER = models.PositiveIntegerField('OTHER',blank=True,null =True,default=0)
	FL_TOTAL = models.PositiveIntegerField('LOADED FULL TEU',blank=True,null =True,default=0)
	
	#loaded-MT
	MTL_20DR = models.PositiveIntegerField('20DR',blank=True,null =True,default=0)
	MTL_20RF = models.PositiveIntegerField('20RF',blank=True,null =True,default=0)
	MTL_40DR = models.PositiveIntegerField('40DR',blank=True,null =True,default=0)
	MTL_40RF = models.PositiveIntegerField('40RF',blank=True,null =True,default=0)
	MTL_45HC = models.PositiveIntegerField('45HC',blank=True,null =True,default=0)
	MTL_OTHER = models.PositiveIntegerField('OTHER',blank=True,null =True,default=0)
	MTL_TOTAL = models.PositiveIntegerField('LOADED MT TEU ',blank=True,null =True,default=0)

	
	date_added = models.DateTimeField(auto_now_add = True)
        date_updated = models.DateTimeField (auto_now=True,blank =True, null = True)

	
	
        def __unicode__ (self):
		return '%s [ %s ]' %(self.VOYAGE,self.PORT.PORT)

	def discharge_full(self): #net
		self.FD_TOTAL = "%s" %(self.FD_20DR +self.FD_20RF +(2 * self.FD_40DR) + (2 * self.FD_40RF))
		#self.save()
		return "%s" %(self.FD_TOTAL)


	def discharge_empty(self): #net
		self.MTD_TOTAL = "%s" %(self.MTD_20DR +self.MTD_20RF +(2 * self.MTD_40DR) + (2 * self.MTD_40RF))
		#self.save()
		return "%s" %(self.MTD_TOTAL)

	def loaded_full(self): #net
		self.FL_TOTAL = "%s" %(self.FL_20DR +self.FL_20RF +(2 * self.FL_40DR) + (2 * self.FL_40RF))
		#self.save()
		return "%s" %(self.FL_TOTAL)

	def loaded_empty(self): #net
		self.MTL_TOTAL = "%s" %(self.MTL_20DR +self.MTL_20RF +(2 * self.MTL_40DR) + (2 * self.MTL_40RF))
		#self.save()
		return "%s" %(self.MTL_TOTAL)
	
	def total_loaded(self):
		self.loaded_total =  "%s" %( int(self.loaded_empty()) + int(self.loaded_full() ))
		return "%s" %(self.loaded_total)

	def total_discharge(self):
		self.discharge_total =  "%s" %( int(self.discharge_empty()) + int(self.discharge_full() ))
		return "%s" % (self.discharge_total)
	
	def total_cargo(self):
		self.SUM =  "%s" %( int(self.total_discharge()) + int(self.total_loaded() ))
		return self.SUM
	
	def calculate_total(self): #total
		total = 0;
		for teu in self.all():
			total += teu.SUM;
		return total;

	def save(self,*args,**kwargs):
		
		#self.presupuesto.total = self.presupuesto.calclular_total()
		#self.budget.total = self.budget.calclular_total()  
		self.discharge_full()  
		self.discharge_empty()
		self.loaded_full()
		self.loaded_empty()
		self.total_loaded()
		self.total_discharge()
		self.total_cargo()
    		super(Cargo,self).save(*args, **kwargs)
		#self.presupuesto.save()
		return True

class Position(models.Model):
	SHIP = models.ForeignKey(Ship_details,related_name='ShipName')
	VOYAGE = models.ForeignKey(Voyage)
	
	SP =  models.CharField('S/P',choices=(("Sea","Sea"),("Port","Port")),max_length = 20,default=" ")
	TYPE = models.CharField('type',choices=(("SSP","SSP"),("ESP","ESP"),("ANCHOR","ANCHOR"),("ALL FAST","ALL FAST"),("CAST OFF","CAST OFF")),max_length = 20,default="ANCHOR")
	DATE_RE = models.DateTimeField('Date of Report')
	TIME_RE = models.TimeField('Time of Report')
	LATITUDE = models.FloatField('Latitude')
	LONGITUDE = models.FloatField('Longitude')
	ORIGIN_PORT = models.ForeignKey(Port,related_name='Port1',blank = True, null = True)
	DESTINATION = models.ForeignKey(Port,related_name='Port2',blank = True, null = True)
	ETA_DATE = models.DateField('ETA Date',blank = True, null = True)
	ETA_TIME = models.TimeField('ETA Time',blank = True, null = True)
	ETA_LOCALTIME = models.TimeField('Local Time',blank = True, null = True)
	DIST_DIALY = models.FloatField('Distance Daily',blank = True, null = True)
	DIST_VOYAGE = models.FloatField('Distance Voyage',blank = True, null = True)
	DIST_REMAINING = models.FloatField('Distance Remaining',blank = True, null = True)
	DIST_PORT = models.FloatField('Distance Port',blank = True, null = True)
	HOURS_DAILY = models.FloatField(blank = True, null = True)
	HOURS_VOYAGE = models.FloatField(blank = True, null = True)
	HOURS_MAN = models.FloatField(blank = True, null = True)
	HOURS_PORT = models.FloatField(blank = True, null = True)
	SPEED_DAILY = models.FloatField(blank = True, null = True)
	SPEED_VOYAGE = models.FloatField(blank = True, null = True)
	ROB_IFO  = models.FloatField(blank = True, null = True)
	ROB_MGO  = models.FloatField(blank = True, null = True)
	ROB_FW  = models.FloatField(blank = True, null = True)
	ROB_BALLAST  = models.FloatField(blank = True, null = True)
	LIFTED_IFO  = models.FloatField(blank = True, null = True)
	LIFTED_MGO  = models.FloatField(blank = True, null = True)
	LIFTED_FW  = models.FloatField(blank = True, null = True)
	CONSUMPTION_IFO = models.FloatField(blank = True, null = True)
	CONSUMPTION_MGO = models.FloatField(blank = True, null = True)
	CONSUMPTION_FW = models.FloatField(blank = True, null = True)

	date_added = models.DateTimeField(auto_now_add = True)
        date_updated = models.DateTimeField(auto_now_add = True)

        def __unicode__ (self):
		return '%s [%s] ' %(self.VOYAGE,self.DATE_RE)




class VoyageChangeForm(ModelForm):
    class Meta:
       
        widgets = {
            'V_DATE':SuitDateWidget,
            
            
        }
class PositionChangeForm(ModelForm):
    class Meta:
       
        widgets = {
            'LONGITUDE':EnclosedInput(append='.<sup>0</sup>',attrs={'class': 'input-mini'}),
             'LATITUDE': EnclosedInput(append='.<sup>0</sup>',attrs={'class': 'input-mini'}),
             'DIST_DIALY': EnclosedInput(prepend='icon-globe', append='km',attrs={'class': 'input-mini'}),
             'DIST_VOYAGE': EnclosedInput(prepend='icon-globe', append='km',attrs={'class': 'input-mini'}),
             'DIST_REMAINING': EnclosedInput(prepend='icon-globe', append='km',attrs={'class': 'input-mini'}),
             'DIST_PORT': EnclosedInput(prepend='icon-globe', append='km',attrs={'class': 'input-mini'}),
             'HOURS_DAILY': EnclosedInput(prepend='icon-globe', append='H',attrs={'class': 'input-mini'}),
             'HOURS_VOYAGE': EnclosedInput(prepend='icon-globe', append='H',attrs={'class': 'input-mini'}),
             'HOURS_MAN': EnclosedInput(prepend='icon-globe', append='H',attrs={'class': 'input-mini'}),
             'HOURS_PORT': EnclosedInput(prepend='icon-globe', append='H',attrs={'class': 'input-mini'}),
             'SPEED_DAILY': EnclosedInput(prepend='icon-globe', append='knot',attrs={'class': 'input-mini'}),
             'SPEED_VOYAGE': EnclosedInput(prepend='icon-globe', append='knot',attrs={'class': 'input-mini'}),
        }

class CargoChangeForm(ModelForm):
    class Meta:
       
        widgets = {
            'FD_20DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'FD_20RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'FD_40DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'FD_40RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'FD_45HC':EnclosedInput(append='HC',attrs={'class': 'input-mini'}),
            'FD_OTHER':EnclosedInput(append='FO',attrs={'class': 'input-mini'}),
            'MTD_20DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'MTD_20RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'MTD_40DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'MTD_40RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'MTD_45HC':EnclosedInput(append='HC',attrs={'class': 'input-mini'}),
            'MTD_OTHER':EnclosedInput(append='OTHER',attrs={'class': 'input-mini'}),
            'MTD_TOTAL':EnclosedInput(append='TOTAL',attrs={'class': 'input-mini'}),
            
            
            'FL_20DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'FL_20RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'FL_45HC':EnclosedInput(append='HC',attrs={'class': 'input-mini'}),
            'FL_40DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'FL_40RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'FL_OTHER':EnclosedInput(append='OTHER',attrs={'class': 'input-mini'}),
            'FL_TOTAL':EnclosedInput(append='TOTAL',attrs={'class': 'input-mini'}),
            
            
            'MTL_20DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'MTL_20RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'MTL_45HC':EnclosedInput(append='HC',attrs={'class': 'input-mini'}),
            'MTL_40DR':EnclosedInput(append='DR',attrs={'class': 'input-mini'}),
            'MTL_40RF':EnclosedInput(append='RF',attrs={'class': 'input-mini'}),
            'MTL_OTHER':EnclosedInput(append='OTHER',attrs={'class': 'input-mini'}),
            'MTL_TOTAL':EnclosedInput(append='TOTAL',attrs={'class': 'input-mini'}),
        }


class Port_Admin(admin.ModelAdmin):
	list_display = ('PORT','date_added')
	search_fields = ['PORT']


class Voyage_Admin(admin.ModelAdmin):
	list_display = ('VOYAGE','LEG',)
	list_filter = ('LEG','VOYAGE')
	search_fields = ['VOYAGE','^VOYAGE_CREW__surname']
        filter_horizontal = ['VOYAGE_CREW',]
        form = VoyageChangeForm

class Position_Admin(admin.ModelAdmin):
	form = PositionChangeForm
	list_display = ('VOYAGE','SP','TYPE','DATE_RE','TIME_RE','LATITUDE','LONGITUDE','ORIGIN_PORT','DESTINATION',)
	list_filter = ('VOYAGE','ORIGIN_PORT','DESTINATION','SHIP')
	search_fields = ['VOYAGE']
	fieldsets         = ( (None, {
				
				'fields':(('SHIP','VOYAGE'),'SP','TYPE','DATE_RE','TIME_RE',('LATITUDE','LONGITUDE'),('ORIGIN_PORT','DESTINATION'))}),
				('ETA',{ 'classes':('collapse',),'fields':(('ETA_DATE','ETA_TIME','ETA_LOCALTIME'),)}),
				('DISTANCES',{ 'classes':('collapse',),'fields':(('DIST_DIALY','DIST_VOYAGE'),('DIST_REMAINING','DIST_PORT'),)}),
				('HOURS',{ 'classes':('collapse',),'fields':(('HOURS_DAILY','HOURS_VOYAGE'),('HOURS_MAN','HOURS_PORT'),)}),
				('SPEED',{ 'classes':('collapse',),'fields':(('SPEED_DAILY','SPEED_VOYAGE'),)}),
				('ROB',{ 'classes':('collapse',),'fields':(('ROB_IFO','ROB_MGO'),('ROB_FW','ROB_BALLAST'),)}),
				('LIFTED',{ 'classes':('collapse',),'fields':(('LIFTED_IFO','LIFTED_MGO'),'LIFTED_FW',)}),
				('CONSUMPTION',{ 'classes':('collapse',),'fields':(('CONSUMPTION_IFO','CONSUMPTION_MGO'),'CONSUMPTION_FW',)}),				
)
	 


class Cargo_Admin(admin.ModelAdmin):
	form = CargoChangeForm
	list_display = ('PORT','VOYAGE','discharge_full','discharge_empty','loaded_full','loaded_empty','total_discharge','total_loaded','SUM','date_added','date_updated')
	readonly_fields = ['SUM','FD_TOTAL','MTD_TOTAL','FL_TOTAL','MTL_TOTAL','loaded_total','discharge_total']
	search_fields = ['PORT']
	#list_filter = ('discharge_full','discharge_empty','loaded_full','loaded_empty',)
        fieldsets         = ( (None, {
        			'classes': ('suit-tab suit-tab-general',),
        			'fields':
                               ('PORT','VOYAGE','V_DATE','SUM','discharge_total','loaded_total',)}),
                               
			      ('DISCHARGE-FULL', {
			      'classes': ('suit-tab suit-tab-DISCHARGE_FULL',),
			      'fields':
                               (('FD_20DR','FD_20RF'),('FD_45HC','FD_40DR'),('FD_40RF','FD_OTHER'),'FD_TOTAL',)}),
      				
				('DISCHARGE-MT', {
				'classes': ('suit-tab suit-tab-DISCHARGE_MT',),
				'fields':
                               (('MTD_20DR','MTD_20RF'),('MTD_45HC','MTD_40DR'),('MTD_40RF','MTD_OTHER'),'MTD_TOTAL',)}),
                              
	                      ('LOADED-FULL', {
	                      'classes': ('suit-tab suit-tab-LOADED_FULL',),
	                      'fields':
                               (('FL_20DR','FL_20RF'),('FL_45HC','FL_40DR'),('FL_40RF','FL_OTHER'),'FL_TOTAL',)}),
      				
				('LOADED-MT', {
				'classes': ('suit-tab suit-tab-LOADED_MT',),
				'fields':
                               (('MTL_20DR','MTL_20RF'),('MTL_45HC','MTL_40DR'),('MTL_40RF','MTL_OTHER'),'MTL_TOTAL',)}),
					)
        date_hierarchy    = 'date_added'
        suit_form_tabs = (('general', 'General'), ('DISCHARGE_FULL', 'DISCHARGE FULL'),
                 ('DISCHARGE_MT', 'DISCHARGE MT'),('LOADED_FULL', 'LOADED FULL'),('LOADED_MT', 'LOADED MT'))
	
	
	
      

admin.site.register(Port,Port_Admin)
admin.site.register(Voyage, Voyage_Admin)
admin.site.register(Position, Position_Admin)
admin.site.register(Cargo,Cargo_Admin)
