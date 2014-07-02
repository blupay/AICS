from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
	Name_of_department = models.CharField(max_length = 30)
      	description        = models.TextField(blank =True, null = True)
      	datecreated=models.DateTimeField(auto_now_add=True,blank=True,null=True)
     	dateupdated=models.DateTimeField(auto_now=True,blank=True,null=True)
	
	def __unicode__(self):
           	 return self.Name_of_department





class Aics_User(models.Model):
      username		= models.CharField(max_length=30,blank=False,null=False)
      firstname		 = models.CharField(max_length=30,blank=True,null=True)
      lastname = models.CharField(max_length=30,blank=True,null=True)
      email = models.EmailField(max_length=50,unique=True,blank=True,null=True)
      mobile_number =models.CharField(max_length=10,blank=True,null=True)
      department    = models.ForeignKey(Department,blank=True,null=True)
      datecreated=models.DateTimeField(auto_now_add=True,blank=True,null=True)
      dateupdated=models.DateTimeField(auto_now=True,blank=True,null=True)
      # change mobile field attribute
     
      def __unicode__(self):
            return self.username

      class Meta:
		verbose_name 	    = "AICS User"
		verbose_name_plural = "AICS Users"

     #TODO
        #any update should update django users as well
      def save(self,*args,**kwargs):
                try:
		        get_user = User.objects.get(username=self.username)
		        get_user.first_name = self.firstname
		        get_user.last_name = self.lastname
		        get_user.email = self.email
		        get_user.save(*args,**kwargs)
			super(Aics_User,self).save(*args, **kwargs)
                except User.DoesNotExist:
                	super(Aics_User,self).save(*args, **kwargs)
                return True




class Aics_User_Admin(admin.ModelAdmin):
      list_display = ('username', 'firstname','lastname', 'email', 'mobile_number','department','datecreated','dateupdated')
      list_filter = ( 'username', 'datecreated','email')
      ordering = ['datecreated']
      search_fields = ['username','lastname','email','department','mobile_number','firstname']
      fieldsets         = ( ("User Details", {'fields':('username','firstname','lastname', 'email', 'mobile_number','department',)}),)
      readonly_fields       = ('username',)

admin.site.register(Department)
admin.site.register(Aics_User,Aics_User_Admin)


