from django.db import models
from django.contrib import admin
from countries.models import Country
from django.contrib.auth.models import User
from datetime import datetime,date,time

# Create your models here.


class Ship_details(models.Model):
	ship_ID         =  models.AutoField(primary_key=True,editable = False)
	ship_name       =  models.CharField("Ship's Name",max_length = 30,help_text ="This designates the ship Name")
	owner           = models.CharField('Ship Owner', max_length = 30, blank = True, null = True, help_text = "The owner of the ship")
	ship_manager    = models.CharField('Ship Manager', max_length = 15, blank = True, null = True, help_text = "The ship manager")
	call_sign       =  models.CharField('Call Sign',max_length = 30,help_text ="Transmission code")
	mmsi            =  models.CharField('MMSI',max_length = 9,help_text ="Maritime Mobile Service Identify")
	nationality     =  models.ForeignKey("Nationality",Country, default = "GH")	
	port_of_register =  models.ForeignKey("Port of Register",Country, default = "GH")
	official_number  =  models.CharField("Official Number",max_length = 15,help_text ="Official number")
	imo_number       = models.CharField("IMO Number",max_length = 7,help_text ="International Maritime Organisation")	
	built            = models.CharField('Built', max_length = 60,blank = True, null = True,help_text = "The name of the manufacturer")	
	year_built       =  models.PositiveIntegerField("Year of manufacture",blank = True, null = True,help_text ="Year of manufacture")
	design           = models.CharField("Class", max_length = 7, help_text = "The kind of ship")
	register         = models.CharField('Register', max_length = 30,blank = True, null = True)
	type1            =  models.CharField('Type',max_length = 30,help_text ="Type of vessel")	
	propeller        =  models.CharField('Propeller', 
					   choices =(("Variable Pitch Propeller","Variable Pitch Propeller"),
                                                     ("Skewback Propeller","Skewback Propeller"),
                                                     ("Modular Propeller","Modular Propeller")),
                                            max_length = 15)
	cranes           = models.CharField ("Cranes", max_length = 30, help text="Type of crane on the ship")
	standard         = models.PositiveIntegerField ("Standard",blank = True, null = True,help_text ="Measured in metric tonnes(mtns)")
	heavy_lift       =  models.CharField("Heavy Lift", max_length = 11, help_text="XXX/XXX tonnes(mtns)")
	
     	
	


	class Meta:
		verbose_name 	    = "Ship Details"
		verbose_name_plural = "Ship Details"
		

class Dimension(models.Model):
	length_overall     	= models.PositiveInteger("Length Overall",blank = True, null = True,help_text ="Measured in metres(m)")
	length_bp     		= models.PositiveInteger("Length BP",blank = True, null = True,help_text ="Measured in metres(m)")
	breadth     		= models.PositiveInteger("Breadth",blank = True, null = True,help_text ="Measured in metres(m)")
	summer_draught    	= models.PositiveInteger("Summer Draught",blank = True, null = True,help_text ="Measured in metres(m)")
	depth_to_deck    	= models.PositiveInteger("Depth to upper Deck",blank = True, null = True,help_text ="Measured in metres(m)")
	hold_dimension    	= models.CharField("Hold Dimension",max_length = 30, help_text ="XX.XX x XX.XX x XX.XX metres(m)")
	cargo_space    		= models.PositiveInteger("Cargo Voice Space",blank = True, null = True,help_text ="Measured in cubic metre(cub.m)")
	top_mast    		= models.PositiveInteger("Top Mast",blank = True, null = True,help_text ="Measured in metres(m),height above keel")
	fore_mast    		= models.PositiveInteger("Fore Mast",blank = True, null = True,help_text ="Measured in metres(m), height above keel")
	speed_max    		= models.PositiveInteger("Max. Speed",blank = True, null = True,help_text ="Measured in knots")
	consumption_sea    	= models.PositiveInteger("Consumption at Sea",blank = True, null = True,help_text ="Measured in metric tonnes of IFO 380")
	cargo_vol    		= models.PositiveInteger("Cargo hold Volume",blank = True, null = True,help_text ="Measured in cubic metre(cub.m)")





	class Meta:
		verbose_name 	    = "Dimension"
		verbose_name_plural = "Dimensions"



class Tonnage(models.Model):
	gross_tonnage     	= models.PositiveInteger("Gross Tonnage, int",blank = True, null = True,help_text ="Measured in tonnes(t)")
	net_tonnage 		= models.PositiveInteger("Net Tonnage, int",blank = True, null = True,help_text ="Measured in tonnes(t)")
	dead_weight 		= models.PositiveInteger("Deadweight",blank = True, null = True,help_text ="Measured in tonnes(t)")
	displacement   		= models.PositiveInteger("Displacement",blank = True, null = True,help_text ="Measured in tonnes(t)")
	light_ship1    		= models.PositiveInteger("Light Ship(with TWP)",blank = True, null = True,help_text ="Measured in tonnes(t)")
	light_ship2    		= models.PositiveInteger("Light Ship(without TWP)",blank = True, null= True, help_text ="Measured in tonnes(t)")
	tw_pontoons_weight    	= models.PositiveInteger("TW Pontoons weight",blank = True, null = True,help_text ="Measured in tonnes(t)")
	hc_weight 		= models.PositiveInteger("HC weight",blank = True, null = True,help_text ="Measured in tonnes(t)")
	



	class Meta:
		verbose_name 	    = "Tonnage"
		verbose_name_plural = "Tonnages"



class Engine_generator(models.Model):
	main_engine     		= models.CharField("Main Engine",max_length = 30, help_text ="Type of Engine")
	shaft_generator 		= models.CharField("Hold Dimension",max_length = 30, help_text ="number(rpm)")
	diesel_generator 		= models.PositiveInteger("Breadth",blank = True, null = True,help_text ="number of diesel engines")
	emergency_generator   		= models.PositiveInteger("Summer Draught",blank = True, null = True,help_text ="Measured in metres(m)")
	me_power    			= models.PositiveInteger("Depth to upper Deck",blank = True, null = True,help_text ="Measured in metres(m)")
	bow_thruster    		= models.CharField("Hold Dimension",max_length = 30, help_text ="XX.XX x XX.XX x XX.XX metres(m)")
	diesel_gen_capa    		= models.PositiveInteger("Cargo Voice Space",blank = True, null = True,help_text ="Measured in cubic metre(cub.m)")
	emergency_gen_capa  		= models.PositiveInteger("Top Mast",blank = True, null = True,help_text ="Measured in metres(m)")
	#Shaft_gen_capa



	class Meta:
		verbose_name 	    = "Engine_generator"
		verbose_name_plural = "Engine_generators"




class Capacities(models.Model):
	ballast          	= models.PositiveInteger("Length Overall",blank = True, null = True,help_text ="Measured in metres(m)")
	aft_peak 		= models.PositiveInteger("Length BP",blank = True, null = True,help_text ="Measured in metres(m)")
	fresh_water 		= models.PositiveInteger("Breadth",blank = True, null = True,help_text ="Measured in metres(m)")
	fuel_oil   		= models.PositiveInteger("Summer Draught",blank = True, null = True,help_text ="Measured in metres(m)")
	diesel_oil    		= models.PositiveInteger("Depth to upper Deck",blank = True, null = True,help_text ="Measured in metres(m)")
	misc_oil_tank    	= models.CharField("Hold Dimension",max_length = 30, help_text ="XX.XX x XX.XX x XX.XX metres(m)")
	hold    	        = models.PositiveInteger("Cargo Voice Space",blank = True, null = True,help_text ="Measured in cubic metre(cub.m)")
	deck  		        = models.PositiveInteger("Top Mast",blank = True, null = True,help_text ="Measured in metres(m)")
	#total_capacities
	#reefers



	class Meta:
		verbose_name 	    = "Capacities"
		verbose_name_plural = "Capacities"


class Communication(models.Model):
	immarsat_c     	= models.PositiveInteger("Length Overall",blank = True, null = True,help_text ="Measured in metres(m)")
	immarsat_f77v   = models.PositiveInteger("Length BP",blank = True, null = True,help_text ="Measured in metres(m)")
	immarsat_f77f   = models.PositiveInteger("Breadth",blank = True, null = True,help_text ="Measured in metres(m)")
	email		= models.PositiveInteger("Summer Draught",blank = True, null = True,help_text ="Measured in metres(m)")
	gsm_phone    	= models.PositiveInteger("Depth to upper Deck",blank = True, null = True,help_text ="Measured in metres(m)")
	



	class Meta:
		verbose_name 	    = "Capacities"
		verbose_name_plural = "Capacities"
