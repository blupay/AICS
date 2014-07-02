from django.db import models
from django.contrib import admin
from countries.models import Country
from django.contrib.auth.models import User
from datetime import datetime,date,time
from django.forms import ModelForm,TextInput 
from suit.widgets import SuitDateWidget,LinkedSelect, SuitTimeWidget, SuitSplitDateTimeWidget,HTML5Input,AutosizedTextarea,EnclosedInput
from suit.admin import SortableTabularInline



class Ship_details(models.Model):
	ship_ID        	=  models.AutoField(primary_key=True,editable = False)
	ship_name       =  models.CharField("Ship's Name",max_length = 30,help_text ="This designates the ship Name")
	owner      	= models.CharField('Ship Owner', max_length = 30, blank = True, null = True, help_text = "The owner of the ship")
	ship_manager    = models.CharField('Ship Manager', max_length = 15, blank = True, null = True, help_text = "The ship manager")
	
	call_sign       =  models.CharField('Call Sign',max_length = 30,help_text ="Transmission code")
	mmsi      	=  models.CharField('MMSI',max_length = 9,help_text ="Maritime Mobile Service Identify")
	Nationality    	=  models.ForeignKey(Country, default = "GH")	
	port_of_register     =  models.CharField('Port of Registration', 
					   choices =(("Ghana","Ghana"),
                                                     ("Spain","Spain"),
                                                     ("United States of America","United State of America")),
                                            max_length = 30)
	official_number	=  models.CharField("Official Number",max_length = 15,help_text ="Official number")
	imo_number      = models.CharField("IMO Number",max_length = 7,help_text ="International Maritime Organisation")	
	built 		= models.CharField('Built', max_length = 60,blank = True, null = True,help_text = "The name of the manufacturer")	
	year_built     	=  models.PositiveIntegerField("Year of manufacture",blank = True, null = True,help_text ="Year of manufacture")
	design    	= models.CharField("Class", max_length = 7, help_text = "The kind of ship")
	register        = models.CharField('Register', max_length = 30,blank = True, null = True)
	type1        	=  models.TextField('Type',help_text ="Type of vessel")	
	propeller     	=  models.CharField('Propeller', 
					   choices =(("Variable Pitch Propeller","Variable Pitch Propeller"),
                                                     ("Skewback Propeller","Skewback Propeller"),
                                                     ("Modular Propeller","Modular Propeller")),
                                            max_length = 30)
	cranes  	= models.CharField ("Cranes", max_length = 30, help_text="Type of crane on the ship")
	standard     	= models.PositiveIntegerField ("Standard",blank = True, null = True,help_text ="Measured in metric tonnes(mtns)")
	heavy_lift 	=  models.CharField("Heavy Lift", max_length = 11, help_text="XXX/XXX tonnes(mtns)")
	
	#Dimension
	length_overall  = models.FloatField("Length Overall",default=0.0,blank = True, null = True,help_text ="Measured in metres(m)")
	length_bp     		= models.FloatField("Length BP",default=0.0,blank = True, null = True,help_text ="Measured in metres(m)")
	breadth     		= models.FloatField("Breadth",default=0.0,blank = True, null = True,help_text ="Measured in metres(m)")
	summer_draught    	= models.FloatField("Summer Draught",blank = True, default=0.0, null = True,help_text ="Measured in metres(m)")
	depth_to_deck    	= models.FloatField("Depth to upper Deck",default=0.0,blank = True, null = True,help_text ="Measured in metres(m)")
	hold_dimension    	= models.CharField("Hold Dimension",max_length = 30, help_text ="XX.XX x XX.XX x XX.XX metres(m)")
	cargo_space    		= models.FloatField("Cargo Voice Space",default=0.0, blank = True, null = True,help_text ="(Unit(cubic metres))")
	top_mast    		= models.FloatField("Top Mast",default=0.0, blank = True, null = True,help_text ="height above keel(m)")
	fore_mast    		= models.FloatField("Fore Mast",default=0.0, blank = True, null = True,help_text ="height above keel(m)")
	speed_max    		= models.FloatField("Max. Speed",default=0.0,blank = True, null = True,help_text ="Measured in knots")
	consumption_sea    	= models.FloatField("Consumption at Sea",default=0.0,blank = True, null = True,help_text ="metric tonnes(IFO 380)")
	cargo_vol    		= models.FloatField("Cargo hold Volume",default=0.0,blank = True, null = True,help_text ="Measured in cubic metre(cub.m)")
	
	#Tonnage
     	gross_tonnage     	= models.FloatField("Gross Tonnage, int",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	net_tonnage 		= models.FloatField("Net Tonnage, int",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	dead_weight 		= models.FloatField("Deadweight",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	displacement   		= models.FloatField("Displacement",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	light_ship1    		= models.FloatField("Light Ship(with TWP)",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	light_ship2    		= models.FloatField("Light Ship(without TWP)",default=0.0,blank = True, null= True, help_text ="Measured in tonnes(t)")
	tw_pontoons_weight    	= models.FloatField("TW Pontoons weight",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")
	hc_weight 		= models.FloatField("HC weight",default=0.0,blank = True, null = True,help_text ="Measured in tonnes(t)")


	
	# Main Engine and Generators
	main_engine     		= models.CharField("Main Engine",max_length = 30, help_text ="Type of Engine")
	shaft_generator 		= models.CharField("Shaft Generator",max_length = 30, help_text ="number of shaft generators(xxxxrpm)")
	diesel_generator 		= models.PositiveIntegerField("Diesel Generator",blank = True, null = True,help_text ="number of diesel engines              ")
	emergency_generator   		= models.PositiveIntegerField("Emergency Generators",blank = True, null = True,help_text ="Number of Emergency Generators")
	me_power    			= models.CharField("ME Power",max_length = 15 ,help_text ="")
	bow_thruster    		= models.CharField("Bow Thruster",max_length = 15, help_text ="")
	diesel_gen_capa    		= models.CharField("Diesel Generator Capacity",max_length = 15, help_text ="") 
	emergency_gen_capa  		= models.CharField("Emergency Generator Capacity",max_length = 15, help_text ="")
	shaft_gen_capa			= models.CharField("Shaft Generator Capacity",max_length = 15, help_text ="")


#Capacities

	ballast     		= models.FloatField("Ballast, cbm",default =0.0, blank = True, null = True, help_text ="XXXXX.XX(excl. APs)")
	aft_peak 		= models.CharField("After Peak",max_length = 15, help_text ="XXXX / XXX.X cub.m")
	fresh_water 		= models.FloatField("Fresh Water",default =0.0, blank = True, null = True,help_text ="")
	fuel_oil   		= models.CharField("Fuel Oil",max_length = 15, help_text ="")
	diesel_oil    		= models.CharField("Diesel Oil",max_length = 15, help_text ="")
	misc_oil_tank    	= models.FloatField("Misc. Oil Tank",default = 0.0, blank = True, null = True, help_text ="")
	hold    		= models.PositiveIntegerField("Hold",blank = True,default = 0, null = True,help_text ="")
	deck  			= models.PositiveIntegerField("Deck",blank = True,default = 0, null = True,help_text ="")
	total_capacities 	= models.PositiveIntegerField("Total Capacities",blank = True, null = True,help_text ="Generate total capacity of Containers")
	reefers			= models.PositiveIntegerField("Reefers",blank = True, null = True,help_text ="Number of Reefers")
	


#Communication

	inmarsat_c     	        = models.CharField("inmarsat_c  ",max_length = 9, help_text ="")
	inmarsat_f77v		= models.CharField("inmarsat_f77v",max_length = 20, help_text ="")
	inmarsat_f77f		= models.CharField("inmarsat_f77f",max_length = 20, help_text ="")
	email		        = models.EmailField('Email-address',blank = True, null = True)
	gsm_phone    		= models.CharField("GSM Phone",max_length = 15, help_text ="(+XXX) XXX XXX XXXX")

	
        def __unicode__(self):
  	      return '[ SHIP0%s ] %s' %(self.ship_ID,self.ship_name.upper())	


	class Meta:
	      verbose_name 	    = "Ship Details"
	      verbose_name_plural = "Ship Details"


	def Total_Capacity(self):
		if self.hold >= 0 and self.deck >= 0:
			self.total_capacities = "%s" %( float(hold) + float(deck) )
			self.save()
			return "%s" %(self.total_capacities)
		else:
			raise Exception("Invalid numbers for [hold] or [deck] field")


# customise crew form         
class ChangeShipForm(ModelForm):
    class Meta:
       
        widgets = {
            'ship_name': EnclosedInput(prepend='icon-edit',attrs={'class': 'input-large'}),
            'owner': EnclosedInput(prepend='icon-edit',attrs={'class': 'input-large'}),
            'call_sign': EnclosedInput(prepend='icon-lock',attrs={'class': 'input-mini'}),
            'mmsi': EnclosedInput(prepend='icon-flag',attrs={'class': 'input-medium'}),
            'type1': AutosizedTextarea,
            'standard': EnclosedInput(append='mt',attrs={'class': 'input-medium'}),
            'heavy_lift': EnclosedInput(append='mt',attrs={'class': 'input-medium'}),
            'register': EnclosedInput(append='icon-flag',attrs={'class': 'input-medium'}),
            
            #Dimensions
            'length_overall': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'length_bp': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'breadth': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'summer_draught': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'depth_to_deck': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'hold_dimension': EnclosedInput(append='m',attrs={'class': 'input-medium'}),
            'cargo_space': EnclosedInput(append='m<sup>3</sup>',attrs={'class': 'input-mini'}),
            'top_mast': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'fore_mast': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'speed_max': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'consumption_sea': EnclosedInput(append='m',attrs={'class': 'input-mini'}),
            'cargo_vol': EnclosedInput(append='m<sup>3</sup>',attrs={'class': 'input-mini'}),
            
            #Tonnage 
            'gross_tonnage': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'net_tonnage': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'dead_weight': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'displacement': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'light_ship1': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'light_ship2': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'tw_pontoons_weight': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            'hc_weight': EnclosedInput(append='tonnes',attrs={'class': 'input-medium'}),
            
            
            #Main Engine and Generator 
            'main_engine': EnclosedInput(attrs={'class': 'input-large'}),
            'shaft_generator': EnclosedInput(attrs={'class': 'input-large'}),
            'diesel_generator': EnclosedInput(append='icon-pencil',attrs={'class': 'input-mini'}),
            'emergency_generator': EnclosedInput(append='icon-pencil',attrs={'class': 'input-mini'}),
            'me_power': EnclosedInput(append='HP/KW',attrs={'class': 'input-medium'}),
            'bow_thruster': EnclosedInput(append='HP/KW',attrs={'class': 'input-medium'}),
            'diesel_gen_capa': EnclosedInput(append='HP/KW',attrs={'class': 'input-medium'}),
            'emergency_gen_capa': EnclosedInput(append='HP/KW',attrs={'class': 'input-medium'}),
            'shaft_gen_capa': EnclosedInput(append='HP/KW',attrs={'class': 'input-medium'}),
            
             #Capacities
            'ballast': EnclosedInput(append='m<sup>3</sup>',attrs={'class': 'input-medium'}),
            'aft_peak': EnclosedInput(attrs={'class': 'input-medium'}),
            'fresh_water': EnclosedInput(append='m<sup>3</sup>',attrs={'class': 'input-medium'}),
            'fuel_oil': EnclosedInput(append='m<sup>3</sup>/tonnes',attrs={'class': 'input-mini'}),
            'diesel_oil': EnclosedInput(append='m<sup>3</sup>/tonnes',attrs={'class': 'input-mini'}),
            'misc_oil_tank': EnclosedInput(append='m<sup>3</sup>/tonnes',attrs={'class': 'input-mini'}),
            'hold': EnclosedInput(append='TEU',attrs={'class': 'input-mini'}),
            'deck': EnclosedInput(append='TEU',attrs={'class': 'input-mini'}),
            'total_capacities': EnclosedInput(append='icon-edit',attrs={'class': 'input-mini'}),
            'reefers': EnclosedInput(append='icon-edit',attrs={'class': 'input-mini'}),
            
            #Communication
            'email': EnclosedInput(append='icon-envelope',attrs={'class': 'input-large'}),
          
        
            
            
        }




class Ship_details_Admin(admin.ModelAdmin):
      form = ChangeShipForm
      list_display      =('ship_name','ship_manager','call_sign','mmsi','Nationality','port_of_register','official_number','imo_number','built','year_built','design')
      search_fields     = ['ship_ID','ship_name','owner','ship_manager','call_sign','mmsi','official_number','imo_number','register']
      list_filter       = ('port_of_register','year_built',)
      ordering          = ('year_built',)
      classes           = ('collapse closed',)
      #date_hierarchy    = 'date_registered'
      fieldsets         = ( (None, {
      					'classes': ('suit-tab suit-tab-general',),
      					'fields':('ship_name','owner',('call_sign','mmsi'),('Nationality','port_of_register'),'official_number','imo_number',('built','year_built'),'ship_manager'),}),
                    			     ('Advanced details',{ 'classes':('suit-tab suit-tab-general','collapse closed',),'fields':(('design','register'),'type1',('propeller','cranes'),'standard','heavy_lift',),}),
					     ('Dimensions',{ 'classes':('suit-tab suit-tab-Dimensions',),'fields':    (('length_overall','length_bp','breadth'),'summer_draught','depth_to_deck','hold_dimension','cargo_space','top_mast','fore_mast','speed_max',('consumption_sea','cargo_vol'),)}),					     ('Tonnage',{ 'classes':('suit-tab suit-tab-Tonnage',),'fields':(('gross_tonnage','net_tonnage'),'dead_weight','displacement','light_ship1','light_ship2',('tw_pontoons_weight','hc_weight'),)}),
					     ('Main Engine and Generator',{ 'classes':('suit-tab suit-tab-MEG',),'fields':    (('main_engine','shaft_generator'),'diesel_generator','emergency_generator','me_power','bow_thruster','diesel_gen_capa','emergency_gen_capa','shaft_gen_capa',)}),		
					     			     ('Capacities, cub.m',{ 'classes':('suit-tab suit-tab-Capacities',),'fields':    (('ballast','aft_peak'),('fresh_water','fuel_oil'),'diesel_oil',('misc_oil_tank','hold'),'deck','total_capacities','reefers',)}),
					     ('Communication',{ 'classes':('suit-tab suit-tab-Communication',),'fields':    (('inmarsat_c','inmarsat_f77v'),('inmarsat_f77f'),('email','gsm_phone'),)}),
)
      list_per_page     = 20
      #raw_horizontal_fields = ('',)
      readonly_fields       = ('total_capacities',)
      suit_form_tabs = (('general', 'General'), ('Dimensions', 'Dimensions'),
                 ('Tonnage', 'Tonnage'),('MEG','Main Engine and Generator'),('Capacities','Capacities'),('Communication','Communication'))

admin.site.register(Ship_details, Ship_details_Admin)
