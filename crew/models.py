from django.db import models
from django.contrib import admin
from countries.models import Country
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


#from sorl.thumbnail.admin import AdminImageMixin
#from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.forms import ModelForm,TextInput 
from suit.widgets import SuitDateWidget,LinkedSelect, SuitTimeWidget, SuitSplitDateTimeWidget,HTML5Input,AutosizedTextarea,EnclosedInput
from suit.admin import SortableTabularInline

#from simple_history.models import HistoricalRecords
#from simple_history.admin import SimpleHistoryAdmin
from django.template.defaultfilters import slugify
from datetime import date,time
import datetime,random
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from vessel.models import *
import reversion
import string

# Order of Models
'''
1. Rank Model
2. Crew Model
3. Crew Certifications
4. Crew Contracts

'''

class Rank_Trash(models.Model):
	rank_name = models.CharField(blank = True, null = True, max_length = 40)
       	date_created  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
	
	def __unicode__(self):
		return self.rank_name

#Rank Model
class Rank(models.Model):
       	rank = models.CharField(blank = True, null = True, max_length = 40)
       	date_created  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
	
	def __unicode__(self):
		return self.rank
	def delete(self,*args,**kwargs):
		print 43
		get_trash = Rank_Trash(rank_name= self.rank)
		#get_trash.rank_name = self.rank
		print get_trash
		print 32
		get_trash.save()
		super(Rank,self).delete(*args,**kwargs)
		return True
		
	def number_of_crew(self):
	      rank_objects =  Crew_detail.objects.filter(rank__rank = self.rank)
              return "%s" %(rank_objects.count())            
		
#Crew Model
class Crew_detail(models.Model):
	crew_ID        =  models.CharField('Generated ID',help_text='This ID is generated on first creation',unique = True, max_length=30,blank=True,null=True)
	nickname       =  models.CharField('Nick Name',blank = True, null = True, max_length = 30,help_text ="This designates the Nick Name of the Crew")
	surname        =  models.CharField('Surname',max_length = 30,help_text ="This designates the Last name of the Crew")
	othernames     =  models.CharField('Othername(s)',max_length = 30,help_text ="This designates the othername(s) of the Crew")
	slug	       =  models.SlugField('hash key',unique=True,editable=False) #contains unique haskkey for each crew on first save
	no_of_identity =  models.CharField('Number of Identity',max_length = 15, help_text ="Nature and No. of Identity document (seaman book)")
	age            =  models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
	sex            =  models.CharField('Gender', choices =(("Male","Male"),("Female","Female")),max_length = 7)
	Nationality    =  models.ForeignKey(Country, default = "GH", related_name = "counTry")
	rank           =  models.ForeignKey(Rank, related_name = 'ranK',blank = True, null = True)
	'''
	speciality     =  models.CharField('Rank', 
					   choices =(("Captain","Captain"),
                                                     ("Cook","Cook"),
                                                     ("Machine Head","Machine Head"),
                                                     ("Boat Swain","Boat Swain"),
                                                     ("Master","Master"),
                                                     ("Bosun","Bosun"),
                                                     ("Ch./Offr","Ch./offr"),
                                                     ("2nd./Offr","2nd./Offr"),
                                                     ("Ch./Engr","Ch./Engr"),
                                                     ("A.B-1","A.B-1"), 
                                                     ("A.B-2","A.B-2"),
                                                     ("A.B-3","A.B-3"),
                                                     ("Fitter","Fitter"),
                                                    
                                                     ("Supt./Engr","Supt./Engr"),
                                                     ("Sailor","Sailor")),
                                            max_length = 15)
        '''
	marital_status =  models.CharField('Marital Status', 
					   choices =(("Married","Married"),
                                                     ("Divorced","Divorced"),
                                                     ("Widowed","Widowed"),
                                                     ("Single","Single"),
                                                     ("Cohabiting","Cohabiting"),
                                                     ("Civil_Union","Civil Union"),
                                                     ("Domestic_Partnership","Domestic Partnership")),
                                          max_length = 20)
	date_Of_birth  =  models.DateField(blank = True, null = True,help_text = "DD/MM/YYYY")
	place_Of_birth =  models.CharField("Place Of Birth", max_length = 30, blank = True, null = True, help_text="City/Town")
	religion       =  models.CharField('Religion', blank =True, null = True,
                                            choices =(("Christianity","Christianity"),
                                                      ("Islam","Islam"),
                                                      ("Buddhism","Buddhism"),
						      ("Hinduism","Hinduism"),
						      ("Judaism","Judaism"),
						      ("Rastafari_Movement","Rastafari Movement"),
						      ("Jainism","Jainism"),
						      ("Shinto","Shinto"),
						      ("Other","Other")),
					     max_length = 20)
	blood_group   = models.CharField('Blood Group', blank =True, null = True,
                                          choices =(("O+","O+"),
                                                    ("A+","A+"),
                                                    ("B+","B+"),
						    ("AB+","AB+"),
						    ("O-","O-"),
                                                    ("A-","A-"),
                                                    ("B-","B-"),
						    ("AB-","AB-")),
					     max_length = 3)
	res_Address    = models.TextField('Residential Address', max_length = 60,blank = True, null = True,help_text = "")
	next_of_kin    = models.TextField("Next of kin",blank = True, null = True,help_text = "NAME, ADDRESS( IF DIFFERENT), RELATIONSHIP,MOBILE")
	mobile         = models.CharField('Mobile', max_length = 30, blank = True, null = True,unique =  True, help_text = "")
        email          = models.EmailField('Email-address',blank = True, null = True)
        ship           = models.ForeignKey(Ship_details,help_text = "Select Ship",blank = True, null = True)
        employment_date  = models.DateField(blank= True, null = True)
	date_registered  = models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated     = models.DateTimeField (auto_now=True,blank =True, null = True)
        head_shot	 = FilerImageField(null=True, blank=True)
        added_by   	 = models.CharField(max_length = 50,blank=True, null = True)
        last_updated_by       = models.CharField(max_length = 50,blank=True, null = True)

	class Meta:
		verbose_name 	    = "Crew Personal Details"
		verbose_name_plural = "Crews Personal Details"
		
	#Not complete-function to check how long the crew have been working- generated from employment date
	def worked_for(self):
		print self.employment_date.strftime("%Y-%m-%d")
		print datetime.now().strftime("%Y-%m-%d")
		print 1
		fmt = "%Y-%m-%d"
                d1 = datetime.strptime(str(self.employment_date.strftime(fmt)), fmt)
                print 2
                d2 = datetime.strptime(str(datetime.now().strftime(fmt)), fmt)
                print 3
                datediff = d2 - d1
                print 4
                print datediff
                print 5
                 
                if datediff.days/365 ==0:
                     yearsSpent = datediff
                    
                else:
                     yearsSpent =datediff.days/365
                     yearsSpent = str(yearsSpent)+" Year(s)"
	       	#if self.employment_date:
	           	 #datediff= (datetime.now().strftime("%Y-%m-%d"))-(self.employment_date.strftime("%Y-%m-%d"))
	           	 
	       	return yearsSpent

	# view function
	def Details(self):
	      return "view"
	      
	#function to return the full name of crew
	def Full_name_(self):
              	return "%s %s " %(self.surname.upper(),self.othernames.upper())
		
	#function th generate crew ID	
        def gen_ID(self):
                if self.crew_ID  == None:
			id_gen = random.randint(10,40)
                	id_gen1 = random.randint(50,90)
                	id_gen2 = random.randint(30,80)     
                	self.crew_ID = "%s%s%s%s" %(self.surname[:2].upper(),id_gen,id_gen1,id_gen2)
                else:
                     return self.crew_ID
                     
	def __unicode__(self):
	      return '[ %s ] %s' %(self.crew_ID, self.nickname.upper())
	      
	#function to format surname and othernames to upper case
	def to_upper(self):
	     	if self.surname:
	     		self.surname = self.surname.upper()
	     	if self.othernames:
	     		self.othernames = self.othernames.upper() 
	     	if self.no_of_identity:
	     		self.no_of_identity = self.no_of_identity.upper()
	     	return True
	     	
	#Date of birth should not be today or higher- age function-not complete
	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
	         	 yearOfBirth = int(self.date_Of_birth.strftime("%G"))
	         	 
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			 return "%s" %(self.age)
                             
			 else:
				 return ValueError
          	elif self.age and int(self.age[0:3])<=120:
	        	self.date_Of_birth = None
		        return True
	# generate Key
	def id_generator(self,size=20, chars=string.ascii_lowercase + string.digits):
	        if self.slug =='':
	    	     self.slug =''.join(random.choice(chars) for x in range(size))
	    	else:
	    		return self.slug
	    
	# save function
	def save(self,*args,**kwargs):
		self.to_upper()
		self.Age() 
		self.gen_ID()
		self.id_generator()
    		super(Crew_detail,self).save(*args, **kwargs)
		
		return True
	
	

		
class Crew_Certification(models.Model):
	module_number  =  models.AutoField(primary_key=True,editable = False)
	crew           =  models.ForeignKey(Crew_detail, related_name = "CREW",blank = False, null =  False, help_text = "Select a registered Crew")
	module_name    =  models.CharField('Module Name',max_length = 30,help_text ="This designates the certification name")
	description    =  models.TextField('Description',blank = True, null =  True, max_length = 100, help_text = "Certificate description")
	category       =  models.CharField('Category', 
					   choices =(("USCG","US Coast Guard"),
                                                     ("MEBA","MEBA"),
                                                     ("NCLA","NCLA"),
                                                     ("STCW-BASIC","STCW-BASIC"),
                                                     ("Vessel Specific","Vessel Specific"),
                                                     ("Medical Cert.","Medical Cert."),
                                                     ("Other","Other")),
                                          max_length = 20)
        other_category =  models.CharField(help_text ="if Other", max_length =30, blank = True, null=  True)
        
	issue_date     =  models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
	expire_date    =  models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
        date_added     =  models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated   =  models.DateTimeField (auto_now=True,blank =True, null = True)
	added_by   	 = models.CharField(max_length = 50,blank=True, null = True)
        last_updated_by       = models.CharField(max_length = 50,blank=True, null = True)




        def attachment(self):
              return "%s" %(self.crew_cert_file_set.count())

	def __unicode__(self):
    		return "%s [%s]" %(self.module_number,self.crew.crew_ID)
	
	def Module_(self):
	        return "Click to edit"
	
	
	class Meta:
		verbose_name 	    = "Crew Certification"
		verbose_name_plural = "Crew Certifications"
		
        #Check whether certificate has expired or not
        def expire_status(self):
                print self.expire_date
                print 342
                if self.expire_date == None:
                      return None
		elif self.expire_date <= date.today():
		        return False 
		else:
		        return True
 	
        expire_status.boolean = True 
        
        def crew_(self):
           return "%s, %s" %(self.crew.surname,self.crew.othernames)
     
	def Description_(self):
	     return "%s" %(self.description)	              


# Crew Certificates File Upload model            
class Crew_Cert_file(models.Model):
      file_number        		= models.AutoField(primary_key=True)
      Upload_file        		= FilerFileField()
      certificate 			= models.ForeignKey(Crew_Certification,blank = True, null = True,help_text = "")
      date_added 			= models.DateTimeField (auto_now_add=True, blank =True, null = True)
      date_updated                      = models.DateTimeField (auto_now=True,blank =True, null = True)
      
      def __unicode__(self):
           return '%s'% unicode(self.file_number)
      
      def file_Number(self):
          return "Click to edit-- File #%s" %(self.file_number)
      
      def cert_(self):
          return "%s" % (self.certificate.module_name)
       
      class Meta:
		verbose_name = "Certificate Uploads"
		verbose_name_plural = "Certificates Uploads"               
               
# File upload inline in crew certificates                  
class FileInline(admin.TabularInline):
      model = Crew_Cert_file
      suit_classes = 'suit-tab suit-tab-attachments'
      extra = 2

class CertFileAdmin(admin.ModelAdmin):
      list_display =   ('file_Number','cert_')
      list_filter = ('date_added', 'date_updated')      


class crew_contract(models.Model):
       ID 		=  models.AutoField(primary_key=True,editable = False)
       crew             =  models.ForeignKey(Crew_detail, related_name ="KrewCont", blank = False, null =  False, help_text = "Select a registered Crew") 
       contract_title   =  models.CharField(max_length= 40, blank = False, null =  False)
       description      =  models.TextField(blank = True, null =  True)
       issue_by         =  models.CharField("Issued By",max_length = 70, help_text = "Enter the name/contact of the person who issued the contract",blank= True,null=True)
       issued_date      =  models.DateField(blank=True,null=True)
       valid_until      =  models.DateField(blank=True,null=True)
       comment          =  models.TextField(blank=True, null = True, help_text ="enter when the contract was last renewed")
       date_added       =  models.DateTimeField (auto_now_add=True, blank =True, null = True)
       date_updated     =  models.DateTimeField (auto_now=True,blank =True, null = True)   
       added_by   	 = models.CharField(max_length = 50,blank=True, null = True)
       last_updated_by       = models.CharField(max_length = 50,blank=True, null = True)

       
       
       def __unicode__(self):
    		return "%s" %(self.contract_title)
       
       def Module_(self):
	        return "Click to edit"
       
       def crew_(self):
           return "%s, %s" %(self.crew.surname,self.crew.othernames)
       
       
       def expire_status(self):
           if self.valid_until == None:
           	return  None
           elif self.valid_until <= date.today():
                return False 
           else:
                return True
       expire_status.boolean = True 
           
       class Meta:
		verbose_name 	    = "Crew Contract"
		verbose_name_plural = "Crew Contracts"
      
       def attachment(self):
                return "%s" %(self.contract_file_set.count())	
               
class Contract_file(models.Model):
      file_number        = models.AutoField(primary_key=True)
      Upload_file        = FilerFileField()
      contract 			= models.ForeignKey(crew_contract,blank = True, null = True,help_text = "")
      order                      = models.PositiveIntegerField(blank = True, null = True)
      date_added 		= models.DateTimeField (auto_now_add=True, blank =True, null = True)
      date_updated              = models.DateTimeField (auto_now=True,blank =True, null = True)
      
      def __unicode__(self):
           return '%s'% unicode(self.file_number)
      
      def file_Number(self):
          return "Click to edit" 
      
      def cont_(self):
          return "%s" % (self.contract.contract_title)
       
      class Meta:
		verbose_name = "Contract Uploads"
		verbose_name_plural = "Contract Uploads/files"  

                   
class ContractInline(admin.TabularInline):
      model = Contract_file
      suit_classes = 'suit-tab suit-tab-attachments'
      extra = 2

class ContractFileAdmin(admin.ModelAdmin):
      list_display =   ('file_Number','cont_','date_added','date_updated')
      list_filter = ('date_added','contract','date_updated')      
  
# customise crew form         
class ChangeCrewForm(ModelForm):
    class Meta:
       
        widgets = {
            'date_Of_birth': HTML5Input(input_type='date'),
            'res_Address': AutosizedTextarea,
            'next_of_kin':AutosizedTextarea,
            'employment_date':HTML5Input(input_type='date'),
            'email': EnclosedInput(append='icon-envelope'),
            'rank':LinkedSelect,
            'ship':LinkedSelect,
        }

class CertfileForm(ModelForm):
    class Meta:
       
        widgets = {
            'issue_date': HTML5Input(input_type='date'),
            'description': AutosizedTextarea,
            'expire_date':HTML5Input(input_type='date'),
            
        }
class ContractfileForm(ModelForm):
    class Meta:
       
        widgets = {
            'issue_date': HTML5Input(input_type='date'),
            'description': AutosizedTextarea,
            'comment': AutosizedTextarea,
            'valid_until':HTML5Input(input_type='date'),
            'issued_date':HTML5Input(input_type='date'),
        }
'''                 
class ProductForm(ModelForm):
    class Meta:
        widgets = {

            # Appended by text
            'discount': EnclosedInput(append='%'),
            'size': EnclosedInput(append='m<sup>2</sup>'),

            # By icons
            'email': EnclosedInput(append='icon-envelope'),
            'user': EnclosedInput(prepend='icon-user'),

            # You can also use prepended and appended together
            'price': EnclosedInput(prepend='$', append='.00'),

            # Use HTML for append/prepend (See Twitter Bootstrap docs of supported tags)
            'url': EnclosedInput(prepend='icon-home', append='<input type="button" class="btn"  value="Open link">'),

        }           
'''
# Crew Admin
class Crew_Admin(reversion.VersionAdmin,admin.ModelAdmin):
      form = ChangeCrewForm 
      list_display      =('no_of_identity','Full_name_','nickname','sex','rank','Nationality','mobile','date_Of_birth','age','email','employment_date','worked_for')
      search_fields     = ['othernames','surname','nickname','mobile','no_of_identity']
      list_filter       = ('rank__rank','date_registered')
      ordering          = ('-date_updated',)
      date_hierarchy    = 'date_registered'
      
      fieldsets = [
        ('Personal details', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': [('surname','head_shot'),'othernames','nickname','sex','marital_status','mobile',('date_Of_birth','age')]
        }),
        ('Other details', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['Nationality','res_Address','place_Of_birth','religion','blood_group','next_of_kin']}),
        ('Employment details', {
            'classes': ('suit-tab suit-tab-work',),
            'fields': ['no_of_identity','employment_date','ship','rank','email']}),
         ('Info', {
            'classes': ('suit-tab suit-tab-info',),
            'fields': ['added_by','date_registered','last_updated_by','date_updated','crew_ID','slug']}),
    ]
      
      suit_form_tabs = (('general', 'General'), ('work', 'Employment Details'),
                 ('info', 'Info on Crew'))
      list_per_page     = 20
      readonly_fields   = ('age','added_by','last_updated_by','crew_ID','date_registered','date_updated','slug')
      ordering          = ('surname',)
    
      
      def save_model(self, request,obj,form,change):
             
             obj.last_updated_by = request.user.username
             if  obj.added_by == None:
                        obj.added_by = request.user.username
             obj.save()
      
#Note on Crew Model
'''
Search by either 
1. othernames
2. surname
3. nickname
4. mobile

List display is auto filter by surname

'''   
      
class Certificate_Admin(admin.ModelAdmin):
      form = CertfileForm
      inlines = (FileInline,)
      
      list_display      =('Module_','crew_','module_name','attachment','category','issue_date','expire_date','expire_status')
      search_fields     = ['module_number','^crew__surname','^crew__othernames','^crew__nickname','module_name','category']
      list_filter       = ('category','issue_date','expire_date','date_updated',)
      ordering          = ('-date_updated',)
      date_hierarchy    = 'date_added'
      fieldsets         = ( (None, { 
      			'classes': ('suit-tab suit-tab-details',),
      			'fields':('crew','module_name','description','category','other_category','issue_date','expire_date')}),
      			(None, { 
      			'classes': ('suit-tab suit-tab-attachments',),
      			'fields':('')}),
      			(None, { 
      			'classes': ('suit-tab suit-tab-info',),
      			'fields':('date_added','added_by','date_updated','last_updated_by')}),
      			)
      list_per_page     = 20
      suit_form_tabs    = (('details', 'Details'), ('attachments', 'Attachments'),('info','info'))
      readonly_fields = ('date_added','date_updated','added_by','last_updated_by',)
      
      def save_model(self, request,obj,form,change):
             
             obj.last_updated_by = request.user.username
             if  obj.added_by == None:
                        obj.added_by = request.user.username
             obj.save()

class contract_Admin(admin.ModelAdmin):
      suit_form_tabs    = (('details', 'Details'), ('attachments', 'Attachments'),('info','info'))
      form = ContractfileForm
      list_display      =('Module_','crew_','contract_title','attachment','issue_by','issued_date','expire_status','valid_until')
      
      def save_model(self, request,obj,form,change):
             
             obj.last_updated_by = request.user.username
             if  obj.added_by == None:
                        obj.added_by = request.user.username
             obj.save()
      fieldsets         = ( (None, { 
      			'classes': ('suit-tab suit-tab-details',),
      			'fields':('crew','contract_title','issue_by','issued_date','valid_until','description','comment')}),
      			(None, { 
      			'classes': ('suit-tab suit-tab-attachments',),
      			'fields':('')}),
      			(None, { 
      			'classes': ('suit-tab suit-tab-info',),
      			'fields':('date_added','added_by','date_updated','last_updated_by')}),
      			)
      search_fields     = ['ID','^crew__surname','^crew__othernames','^crew__nickname','contract_title']
      list_filter       = ('issued_date','valid_until','date_updated',)
      ordering          = ('-date_updated',)
      date_hierarchy    = 'date_added'
      list_per_page     = 20
      readonly_fields = ('date_added','date_updated','added_by','last_updated_by',)
      inlines           = (ContractInline,)
      raw_horizontal_fields = ('crew',)

class rank_Admin(admin.ModelAdmin):
 	#actions = None
	list_display      =('rank','number_of_crew','date_created','date_updated')
	list_filter       = ('rank',)
	
class SuitUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        widgets = {
            'last_login': SuitSplitDateTimeWidget,
            'date_joined': SuitSplitDateTimeWidget,
        }


class SuitAdminUser(UserAdmin):
    form = SuitUserChangeForm
    '''
    def queryset(self, request):
        qs = super(SuitAdminUser, self).queryset(request)
        return qs.filter(id=2) if request.user.username == 'admin' else qs

    def response_change(self, request, obj):
        messages.warning(request, 'User data change is prevented in demo mode')
        return super(SuitAdminUser, self).response_change(request, obj)
    '''

admin.site.unregister(User)
admin.site.register(User, SuitAdminUser)


#admin.site.register(Contract_file,ContractFileAdmin)
#admin.site.register(Crew_Cert_file,CertFileAdmin)
admin.site.register(Crew_Certification,Certificate_Admin)
admin.site.register(Crew_detail,Crew_Admin)
admin.site.register(crew_contract,contract_Admin)
admin.site.register(Rank,rank_Admin)
#admin.site.register(Rank_Trash)
