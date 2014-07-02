from django.db import models

# Create your models here.

from django.db import models
from django.contrib import admin
from countries.models import Country
from django.contrib.auth.models import User
from datetime import date,time
import datetime
from inventory.models import *
from aicsUser.models import *



class Crew_Requisition(models.Model):
	requisition_ID		= models.AutoField(primary_key=True, editable=False)
	#item_category		= models.ForeignKey(Ref_Item_Categories)
	'''requisitioner		= models.CharField('Crew Speciality', 
					   choices =(("Captain","Captain"),
                                                     ("Cook","Cook"),
                                                     ("Machine_Head","Machine_Head"),
                                                     ("Boat_Swain","Boat_Swain"),
                                                     ("Sailor","Sailor"),),
                                            max_length = 15)'''
	requisitioner   = models.CharField(max_length = 20)
        department      = models.CharField(max_length = 30,blank =True, null = True)
	#supplier		= models.ForeignKey(Suppliers)
	order_date		= models.DateField(default = datetime.datetime.now(),help_text = "Leave blank if Today",blank = True, null = True)
        status                  = models.CharField('STATUS', 
					   choices =(("Pending Approval","Pending Approval"),
                                                     ("Approved","Approved"),
						     ("Denied","Denied"),
						     ("Received","Received"),
                                                     ),
                                            max_length = 30, default = "Pending Approval")
        check                 = models.BooleanField(default =False, help_text = "Check if Received") 
        Received              = models.CharField(choices = (("YES","YES"),("NO","NO")),default = "NO",max_length = 3)
	order_state           = models.CharField( 
					   choices =(("URGENT","URGENT"),
                                                     ("MINOR","MINOR"),
						     ("CRITICAL","CRITICAL"),
                                                     ),max_length = 30 )
	reason_for_required_item	=  models.TextField('Reason for request',blank = True, null = True,max_length = 40, help_text = "Brief and specific")
	date_added	 = models.DateTimeField (auto_now_add=True, blank =True, null = True)
        date_updated     = models.DateTimeField (auto_now=True, blank =True, null = True)
	
	
	def __unicode__(self):
    		return "%s %s" %(self.requisition_ID,self.date_added.strftime("%b %d, %Y, %I:%M %p"))


	class Meta:
		verbose_name = "Crew Requisition"
		verbose_name_plural = "Crew Requisitions"

	def received(self):
	     if self.check is False:
	          self.Received = "NO"
	     else:
	         self.Received  ="YES"
	
	     
	def save(self,*args,**kwargs):
	        obj1   = Crew_Requisition()
	           
	               
		#self.presupuesto.total = self.presupuesto.calclular_total()
		#self.budget.total = self.budget.calclular_total() 
		#self.Age()
		self.received() 
    		super(Crew_Requisition,self).save(*args, **kwargs)
		#self.presupuesto.save()
		return True
	 
	
	
	

class Crew_Order(models.Model):
	ref		= models.AutoField(primary_key=True, editable=False)
	quantity	= models.PositiveIntegerField('Quantity',default= 0, blank = True, null = True,help_text ="The quantity of items needed")	
	unit		= models.CharField('Unit', max_length=15,blank = True, null = True,help_text ="PCS/VOL/PAIR...")
	item	        = models.ForeignKey(Inventory_Items, related_name="Item_ID2",blank =True, null=True)
	other           = models.CharField(max_length = 50,blank = True, null = True, help_text = "Indicate Item if not in inventory")
	#stock_num	= models.ForeignKey(Item_Stock_Levels)
	#cost		= models.FloatField(blank=True, null=True, default= 0.0)
	#total		= models.FloatField(blank=True, null=True, default= 0.0)
	date_of_order	= models.ForeignKey(Crew_Requisition)
	quote		= models.CharField('Quote', max_length=15,blank = True, null = True,help_text ="")
        date_added	 = models.DateTimeField (auto_now_add=True, blank =True, null = True)
        date_updated     = models.DateTimeField (auto_now=True, blank =True, null = True)
	
	
	

	def order_number(self):
    	      if self.ref <= 9:
    	         return "ORD000%s" %(self.ref)
    	      elif self.ref > 9 and self.ref < 100:
    	         return "ORD00%s" %(self.ref)
    	      elif self.ref > 99 and self.ref <1000:
    	         return "ORD0%s" %(self.ref)
    	      elif self.ref > 999:
    	         return "ORD%s" %(self.ref)
    	      else:
    	         return "ORD%s" %(self.ref)


	def __unicode__(self):
	      if self.ref <= 9:
    	         return '[ ORD000%s ] ' %(self.ref)
    	      elif self.ref > 9 and self.ref < 100:
    	         return '[ ORD00%s ] ' %(self.ref)
    	      elif self.ref > 99 and self.ref <1000:
    	         return '[ ORD0%s ] ' %(self.ref)
    	      elif self.ref > 999:
    	         return '[ ORD%s ] ' %(self.ref)
    	      else:
    	         return '[ ORD%s ] ' %(self.ref)


        '''def Total_Cost(self):
		if self.quantity >= 0 and self.cost >= 0.0:
			self.total = "%s" %( float(self.quantity) * float(self.cost) )
			self.save()
			return "%s" %(self.total)
		else:
			raise Exception("Invalid numbers for [quantity] or [cost] field")'''


	class Meta:
		verbose_name = ("Crew Order")
		verbose_name_plural = ("Crew Orders")
		#ordering = ("Number")

class OrderInline(admin.TabularInline):
      model = Crew_Order
      readonly_fields = ('date_of_order',)
      fieldsets       = (
		(None, {"fields": ('quantity','unit','item','other','quote','date_of_order')}),
		
	)
      #list_display      =('Total_Cost')


class Order_Admin(admin.ModelAdmin):
      list_display      =('ref','quantity','unit','item','quote','date_of_order')
      search_fields     = ['ref','stock_num' ]
      #list_filter       = ('item_ID','supplier_ID','minimum_order_quantity','maximum_order_quantity',)
      list_per_page     = 20

class Crew_Requisition_Admin(admin.ModelAdmin):
	obj = Crew_Requisition()
	#obj1   = Supplies_Requisition()
	def save_model(self,request,obj,form,change):
		try:
			obj1   = Supplies_Requisition.objects.get(pk=obj.pk)
			order  = Crew_Order.objects.filter(instance = obj)
	             
			obj.requisitioner  = request.user.username
			obj1.requisitioner =request.user.username
		
	        	obj1.status = obj.status
	        	obj1.order_state =obj.order_state 
	        	obj1.reason_for_required_item = obj.reason_for_required_item
	        	obj1.Received = obj.Received
			if request.user.is_superuser:
		    		obj.department ="Administration"
		    
			else:
				usn               =  Aics_User.objects.get(username =request.user.username )
				obj.department    = usn.department
			obj1.department= obj.department
			obj.save()
			obj1.save()
		except Supplies_Requisition.DoesNotExist:
			obj1   = Supplies_Requisition()

	     
			obj.requisitioner  = request.user.username
			obj1.requisitioner =request.user.username
		
	        	obj1.status = obj.status
	        	obj1.order_state =obj.order_state 
	        	obj1.reason_for_required_item = obj.reason_for_required_item
	        	obj1.Received = obj.Received
			if request.user.is_superuser:
		    		obj.department ="Administration"
		    
			else:
				usn               =  Aics_User.objects.get(username =request.user.username )
				obj.department    = usn.department
			obj1.department= obj.department
			obj.save()
			obj1.save()
	list_display        = ('requisition_ID','requisitioner','department','order_date','reason_for_required_item','status','Received','order_state','date_added','date_updated')
	list_filter         = ('department','order_state','status')
	#ordering            = ('requisition_ID')
	inlines             = [OrderInline]
	search_fields       = ['requisition_ID','department','requisitioner','order_state','status']
	fieldsets           = ((None, {"fields": ('status','order_state','order_date','reason_for_required_item','check')}),)
	
	readonly_fields = ('requisitioner','status','department')
        date_hierarchy = 'order_date'
        

admin.site.register(Crew_Order,Order_Admin)



admin.site.register(Crew_Requisition,Crew_Requisition_Admin)
