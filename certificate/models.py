from django.db import models
from django.contrib import admin
from datetime import date,time
import datetime

from filer.fields.file import FilerFileField

from django.forms import ModelForm,TextInput 
from suit.widgets import SuitDateWidget,LinkedSelect, SuitTimeWidget, SuitSplitDateTimeWidget,HTML5Input,AutosizedTextarea,EnclosedInput
from suit.admin import SortableTabularInline


		
#
class Certificate(models.Model):
	certificate_code 		= models.CharField(unique = True,max_length =50,help_text = " eg. 005QA")
	document_name 			= models.CharField(max_length =50,help_text = " e.g. MARPOL delivery redbo oils")
	Type_of_Document		= models.CharField(blank = True, null = True,max_length =50,help_text = " e.g. Maintenance certificate,trans-shipment certificate/ documents")
	Number_of_Documents             = models.PositiveIntegerField("Number of Documents",blank = True, null = True)
	Type_of_Technical_info 	        = models.CharField("Type of Technical Info",max_length =50,blank = True, null = True, help_text = "")
	Equipment_or_material 		= models.CharField("Equiment or Material",max_length =50,blank = True, null = True, help_text = " ")
	Agency 				= models.CharField("Agency",max_length =50,blank = True, null = True, help_text = " ")
	Issuedate 			= models.DateField('Issue Date',blank = True, null = True )
	Expiringdate 			= models.DateField('Valid until',blank = True, null = True)
	Last_Annual_Revision_date       = models.DateField("Last Annual Revision Date",blank = True, null = True)
	Classification_Society          = models.CharField("Classification Society",max_length =50,blank = True, null = True,help_text = " eg. LR.LLOYD REGISTER OF SHIP")
	Place                           = models.CharField("Place",max_length =50,blank = True, null = True,help_text = " eg. TEMA HARBOUR")
	External_Reference              = models.TextField('Reference',blank = True, null = True, help_text = "External Reference")
	date_added 			= models.DateTimeField (auto_now_add=True, blank =True, null = True)
        date_updated                    = models.DateTimeField (auto_now=True,blank =True, null = True)
        added_by   	 		= models.CharField(max_length = 50,blank=True, null = True)
        last_updated_by       		= models.CharField(max_length = 50,blank=True, null = True)
        
	def __unicode__ (self):
		return '%s' %(self.document_name.upper())
	
	class Meta:
		verbose_name = "Certificate"
		verbose_name_plural = "Certificates"
	'''	
        def expire_status(self):
           if self.Expiringdate  <= datetime.date.today():
                return False 
           else:
                return True
        expire_status.boolean = True 
        '''
        # CALCULATE THE NUMBER OF YEARS THE CERTIFICATE IS VALID FOR- not complete
        def validity(self):
             Validity_in_years = int(self.Expiringdate.strftime("%G"))- int(datetime.datetime.now().strftime("%G"))
             d1 = datetime.strptime(str(self.Expiringdate.strftime(fmt)), fmt)
             print d1
             if Validity_in_years > 0:
                return "%s years" %(Validity_in_years)
             else:
                fmt = "%Y-%m-%d"
                d1 = datetime.strptime(str(self.Expiringdate.strftime(fmt)), fmt)
                print 2
                print d1
                d2 = datetime.strptime(str(datetime.now().strftime(fmt)), fmt)
                print 3
                print d2
                datediff = d2 - d1
                print datediff
                return datediff           
         
        def attachment(self):
                return "%s" %(self.cert_file_set.count())	    
        
        def days_left(self):
               two_months = datetime.datetime.now() + datetime.timedelta(days=365.25/6)
               return "%s" %(two_months)     
               
class Cert_file(models.Model):
      file_number        = models.AutoField(primary_key=True)
      Upload_file  	 = FilerFileField()
      certificate 			= models.ForeignKey(Certificate,blank = True, null = True,help_text = "")
      date_added 			= models.DateTimeField (auto_now_add=True, blank =True, null = True)
      date_updated                      = models.DateTimeField (auto_now=True,blank =True, null = True)
      
      def __unicode__(self):
           return '%s'% unicode(self.file_number)
      
      def file_Number(self):
          return "Click to edit-- File"
      
      def cert_(self):
          return "%s" % (self.certificate.document_name)
       
      class Meta:
		verbose_name = "File Uploads"
		verbose_name_plural = "File Uploads"               
               
               
                   
class FileInline(admin.TabularInline):
      model = Cert_file
      suit_classes = 'suit-tab suit-tab-attachments'
      extra = 2



class CertfileForm(ModelForm):
    class Meta:
       
        widgets = {
            'Issuedate': HTML5Input(input_type='date'),
            'External_Reference': AutosizedTextarea,
            'Expiringdate':HTML5Input(input_type='date'),
            'date_added':SuitSplitDateTimeWidget,
            'date_updated':SuitSplitDateTimeWidget,
            'Last_Annual_Revision_date':HTML5Input(input_type='date'),
        }

class CertFileAdmin(admin.ModelAdmin):
      list_display =   ('file_Number','cert_')
      list_filter = ('date_added', 'date_updated')       
            
class Certificate_Admin(admin.ModelAdmin):
        form = CertfileForm
	list_display 	= ('certificate_code','document_name','Issuedate','Expiringdate','Last_Annual_Revision_date','validity','attachment')
	list_per_page	 = 20
	list_filter = ('Place', 'Expiringdate', 'Issuedate')
	ordering = ['Expiringdate']
	search_fields = ['document_name','Agency','Expiringdate']
        inlines               = [FileInline]
        
        fieldsets         = ( (None, { 
      			'classes': ('suit-tab suit-tab-details',),
      			'fields':
      			('certificate_code','document_name',
      			'Type_of_Document','Type_of_Technical_info','Equipment_or_material',
      			'Agency','Classification_Society','Place','External_Reference')}),
      			
      			(None, { 
      			'classes': ('suit-tab suit-tab-dates',),
      			'fields':('Issuedate','Expiringdate','Last_Annual_Revision_date')}),
      			
      			(None, { 
      			'classes': ('suit-tab suit-tab-attachments',),
      			'fields':('')}),
      			
      			(None, { 
      			'classes': ('suit-tab suit-tab-info',),
      			'fields':('date_added','added_by','date_updated','last_updated_by')}),
      			
      			)
      	suit_form_tabs    = (('details', 'Details'), ('dates','Dates'),('attachments', 'Attachments'),('info','info'))
      	readonly_fields = ('date_added','date_updated','added_by','last_updated_by',)
	def save_model(self, request,obj,form,change):
             
             obj.last_updated_by = request.user.username
             if  obj.added_by == None:
                        obj.added_by = request.user.username
             obj.save()
      
admin.site.register(Certificate,Certificate_Admin)
#admin.site.register(Cert_file,CertFileAdmin)
