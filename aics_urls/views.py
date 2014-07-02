from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader
from django import  forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from django.forms.models import inlineformset_factory

#from site_content.models import *
from crew.models import *
from certificate.models import *
from aicsUser.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.template.response import TemplateResponse
import datetime
from inventory.models import *


sess_uname = ''
krew = ''
galore=''
two_months = datetime.datetime.now() + datetime.timedelta(days=365.25/6)
seven_days = datetime.datetime.now()-datetime.timedelta(days=7)



class RegisterForm(UserCreationForm):
	#mobile_number = forms.CharField(label = "Mobile Number")
    #department    = forms.CharField(Department)
    #email = forms.EmailField(label = "Email",widget=forms.TextInput(attrs={'placeholder': 'Enter Email Address'}))
    #fullname = forms.CharField(label = "Fullname")
    #firstname = forms.CharField(label = "Firstname")
    #lastname = forms.CharField(label = "Lastname")
	class Meta:
        	model = User
        	exclude=['activation_key','key_expires']
        	fields = ('username', 'first_name','last_name', 'email',)
        	#mobile_number = forms.CharField(label = "Mobile Number")

	
class RegisterForm1(ModelForm):
	class Meta:
		model = Aics_User
		exclude = ['datecreated','dateupdated','username','firstname','lastname', 'email']
        	fields  = ('department','mobile_number',)

def save(self, commit=True):
        form = RegisterForm()
        
        user = super(RegisterForm, self).save(commit=False)
       
        if commit:
            user.save()
        return user



@csrf_exempt
def add_User(request):
    galore=""
    us_n = ""
    p_k = ""
    superuser=""
    try:
    	if request.session["galore"] == "modal":
		us_n = request.session["us_n"]
		p_k = request.session["p_k"] 
		galore = "modal"
		request.session["galore"] = ""
		request.session["us_n"] = ""
                request.session["p_k"] = ""
		
		   
    except KeyError:
	request.session["galore"] = ""

    form = RegisterForm(request.POST)
    form1 = RegisterForm1(request.POST)
    print request.user.is_superuser
    print 3
    if request.method == 'POST':
       
       print request.user.is_superuser
       if form.is_valid() and form1.is_valid():
            new_user = form.save();
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            #login(request, new_user)
            #salt = sha.new(str(random.random())).hexdigest()[:5]
            #activation_key = sha.new(salt+new_user.username).hexdigest()
            #key_expires = datetime.datetime.today() + datetime.timedelta(2)
            worker=Aics_User()
            worker.username = form.cleaned_data["username"]
            worker.firstname = form.cleaned_data["first_name"]
	    worker.lastname =  form.cleaned_data["last_name"]
            worker.email = form.cleaned_data["email"]
            worker.department = form1.cleaned_data["department"]
	    worker.mobile_number = form1.cleaned_data["mobile_number"]
            #worker.activation_key=activation_key
            #worker.key_expires=key_expires
            worker.save()
	    #form1.username = "gggg"
	    #form1.username = form.cleaned_data["username"]
	    #form1.lastname = form.cleaned_data["last_name"]
	    #form1.firstname = form.cleaned_data["first_name"]
	    #form1.email = form.cleaned_data["email"]
            #form1.save()
            request.session["galore"] = "modal"
	    galore = "on"
	    request.session["us_n"] = worker.username
            request.session["p_k"] = new_user.pk
	    p_k="on"
	    us_n = "on"
	    return HttpResponseRedirect('/add_user')
    else:
            if us_n !="" and request.user.is_superuser:
		superuser = "Yes"
		

    return render_to_response("portal/addUser.html", {'superuser':superuser,
						      'us_n':us_n, 
						      'p_k':p_k,
						      'galore':galore, 
						      'form':form, 
				                      'form1' : form1,
						      'user':request.user})


















def portal(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
	else:
		cert_expiring_today  = Certificate.objects.filter(Expiringdate = date.today())	
		cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
		return render_to_response('portal/mainpage.html', {'cert_critical':cert_critical,'cert_expiring_today':cert_expiring_today,'user': request.user})

def main_portal(request):
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
	else:
		cert_expiring_today  = Certificate.objects.filter(Expiringdate = date.today())	 
		Ccont_critical        = crew_contract.objects.filter(valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())		
                allCrew       = Crew_detail.objects.all()
		requisitions_tod = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date = date.today())
     		MaleCrew      = Crew_detail.objects.filter(sex ="Male")
		FemaleCrew    = Crew_detail.objects.filter(sex ="Female")		
		cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
		return render_to_response('portal/base.html', {'cert_critical':cert_critical,'allCrew':allCrew,'MaleCrew':MaleCrew,
								'CrewCont_critical': Ccont_critical ,'FemaleCrew':FemaleCrew,
								'requisitions_tod':requisitions_tod,
								'cert_expiring_today':cert_expiring_today,'user': request.user})



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '    Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '    Enter your password'}))




# Login view - @Nana B.
#tested code and it works logs in perfectly
@csrf_exempt
def do_login(request):
	empty_cred = '' #empty login credential variable
	disabled_accMsg = ''
	invalidMsg = ''
        already_logged_in = ''
        
			
	if request.user.username != '' and request.user.is_superuser:
		return HttpResponseRedirect('/main_portal')
	
	
	if request.method == 'POST':
   	        uname = request.POST['username']	
		pword = request.POST['password']
		if uname == '' or pword == '':
			empty_cred = 'Username or password field cannot be empty!'
		else:
			user = authenticate(username=uname, password=pword)
			#if user.is_staff:
			if user is not None:
				if user.is_superuser:
			        	login(request,user)
					request.session["sess_uname"] = uname
					return HttpResponseRedirect('/main_portal')
				else:
					disabled_accMsg = "Sorry, your account has no access. Contact the administrator."
					
			else:
				invalidMsg = "Username or Password is invalid!"
			#else:
				#disabled_accMsg = "Sorry, your account has been disabled. Contact the administrator."
			#return an invalid login message
	
		#YOUR CODE HERE
	else:
		form = LoginForm()
	form = LoginForm()
	return render_to_response('login/signin.html', {
        'form': form,
        'logged_in': request.user.is_authenticated(),
	'invalidMsg': invalidMsg,
	'empty_cred':empty_cred,
	'disabled_accMsg': disabled_accMsg,
	'user': request.user
        
    })



#LOGOUT - GALORE    
@csrf_exempt
def do_logout(request):
	#if request.user.username != "" and request.user.is_superuser==True:
	#	return HttpResponseRedirect(request.path)
	if request.user.username == '' or request.user.is_active == False:
		request.user.username = ''
		request.session["sess_uname"] = ''
		return HttpResponseRedirect('/')
	try:
    		if request.user.username != '':
			logout(request)
			request.session["sess_uname"] = ''
			request.user.username == ''
			return HttpResponseRedirect('/')
    
		else:
			
			return HttpResponseRedirect('/aics')
		

        except KeyError:
		logout(request)
		request.session["sess_uname"] = ''
		request.user.username == ''
		return HttpResponseRedirect('/')
		




#Change password -OSA
def changedpass(request):
	if request.user.username == '':
		return HttpResponseRedirect('/')
	else:
		return render_to_response('portal/changedpass.html',{'user':request.user})







class ChangPassForm(PasswordChangeForm):
 
	class Meta:
		model = User
		#exclude=['activation_key','key_expires']
		fields = ()




def password_change(request,
                    template_name='portal/changepass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    '''
    if post_change_redirect is None:
        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    '''
    if request.user.username == "" and request.user.is_superuser == False:
    		return HttpResponseRedirect('/')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
	    logout(request)
            return HttpResponseRedirect('/')
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)




		


#CREW VIEW- STEPHEN
def crew(request):
       Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 			= Crew_detail.objects.all()
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       else:
       		
       		return  render_to_response('portal/crew.html',{'cert_critical':cert_critical,
       								'cert_expiring_today':cert_expiring_today ,
       								'Cxp_tod':Cxp_tod ,
       								'crews':crews,
       								'Ccont_critical': Ccont_critical,
       								'user':request.user})
      
      
def crew_list(request):
      
      	term =''
        if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	else:
		crews = Crew_detail.objects.all()
		paginator = Paginator(crews, 6)
		page = request.GET.get('page')
		
    	try:
            crews = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            crews = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            crews = paginator.page(paginator.num_pages)
        cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
        cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
        Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
        Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
        crews_count = Crew_detail.objects.all()
        pop=''
        crew = None
        crew_cert=None
        try:
        	if request.session['term'] !='':
        		term = request.session['term']
        		request.session['term']=''
        		try:
        			if request.session['pop'] =='on':
        			       	pop  = 'on'
        				request.session['pop'] =''
        		except KeyError:
        		          request.session['pop'] =''
        	
        		try:
      				crew = Crew_detail.objects.get(slug=term)
      			except Crew_detail.DoesNotExist:
                		return HttpResponseRedirect('/')
                	try:
			      crew_cert   	 = Crew_Certification.objects.filter(crew__slug = term)
			      xp_tod      	 =  Crew_Certification.objects.filter(crew__slug = term,expire_date= date.today())
			      crew_kontract       = crew_contract.objects.filter(crew__slug = term)
			      cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
			      cert_critical       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
			      Cxp_tod              =  Crew_Certification.objects.filter(expire_date = date.today())
			      crew_cont_critical   =  crew_contract.objects.filter(valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
		      	except Crew_Certification.DoesNotExist:
			      pass
		      	except crew_contract.DoesNotExist:
		      	      pass
		      	except Certificate.DoesNotExist:
		      	      pass
        	
        except KeyError:
        	request.session['term'] =''
        	request.session['pop'] =''
        	        
        return  render_to_response('portal/crewlist.html',
        				{'cert_critical':cert_critical,
        				'cert_expiring_today':cert_expiring_today,
        				'crews':crews,'crew_cert':crew_cert,
        				'crew':crew,
        				'crews_count':crews_count,
        				'Cxp_tod':Cxp_tod,
        				'Ccont_critical':Ccont_critical, 
        				'pop':pop, 
        				'user':request.user})

      
def crew_search(request,term):
	galore = ''
        if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
		
	else:
		if request.GET.get('search_item','') != '':
			term = request.GET.get('search_item','')
			galore = str(term)
	       		crew = Crew_detail.objects.filter(crew_ID__icontains=term)|Crew_detail.objects.filter(nickname__icontains=term)|Crew_detail.objects.filter(surname__icontains=term)|Crew_detail.objects.filter(othernames__icontains=term)
	       		krew = crew
	       		paginator = Paginator(crew, 5)
		        page = request.GET.get('page')
		       
		        
	        else: 
	        	krew = Crew_detail.objects.filter(crew_ID__icontains=galore)|Crew_detail.objects.filter(nickname__icontains=galore)
	      		paginator = Paginator(krew, 5)
		        page = request.GET.get('page')
		        crew = krew
	      		
        
    	try:
            crew = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            crew = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            crew = paginator.page(paginator.num_pages)
        cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
        cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
        Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
        Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
        crews 			= Crew_detail.objects.all()
	return render_to_response('portal/crewSearch.html',{'cert_critical':cert_critical,
					'cert_expiring_today':cert_expiring_today,
					'crew':crew,'krew':krew,'crews':crews,
					'term':term,
					'Cxp_tod':Cxp_tod,
        				'Ccont_critical':Ccont_critical,
					'user':request.user})


def crew_detail(request, term, showDetails):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      print term
      try:
      		crew = Crew_detail.objects.get(slug=term)
      		request.session['term'] = term
      except Crew_detail.DoesNotExist:
                return HttpResponseRedirect('/')
      try:
	      crew_cert   	 = Crew_Certification.objects.filter(crew__slug = term)
	      xp_tod      	 =  Crew_Certification.objects.filter(crew__slug = term,expire_date= date.today())
	      crew_kontract       = crew_contract.objects.filter(crew__slug = term)
	      cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
	      cert_critical       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
	      Cxp_tod              =  Crew_Certification.objects.filter(expire_date = date.today())
	      crew_cont_critical   =  crew_contract.objects.filter(valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
      except Crew_Certification.DoesNotExist:
              pass
      except crew_contract.DoesNotExist:
      	      pass
      except Certificate.DoesNotExist:
      	      pass
      request.session['pop'] = 'on'
      return HttpResponseRedirect('/crew/list/')
      '''
      return render_to_response('portal/crew_detail.html',
      				{'cert_critical':cert_critical,
      				'cert_expiring_today':cert_expiring_today,
      				'crew':crew,
      				'Cxp_tod':Cxp_tod,
      				'xp_tod':xp_tod,
      				'crew_cont_critical':crew_cont_critical,
      				'crew_kontract': crew_kontract,
      				'crew_cert':crew_cert,
      				'user':request.user})
      '''
      						
def crew_xp(request):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:	
      		xp_tod              = Crew_Certification.objects.filter(expire_date = date.today())
                paginator           = Paginator(xp_tod , 5)
                page                = request.GET.get('page')
      try:
            xp_tod = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            xp_tod = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            xp_tod = paginator.page(paginator.num_pages)
      expired_cert        =  Certificate.objects.filter(Expiringdate__lt   = date.today())
      cert_expiring_today =  Certificate.objects.filter(Expiringdate     = date.today())
      cert_critical       =  Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      
      certt		  = Crew_Certification.objects.filter(expire_date = date.today())
      Cxp_tod               =  Crew_detail.objects.filter(CREW__expire_date = date.today())
      crews 		    = Crew_detail.objects.all()
      Ccont_critical        = crew_contract.objects.filter(valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())		
      return render_to_response('portal/crew_certXp.html',
      						{'cert_critical':cert_critical,   						
      						'cert_expiring_today':cert_expiring_today,
      						'expired_cert':expired_cert,'crews':crews,'certt':certt,
      						'xp_tod':xp_tod,
      						'Cxp_tod':Cxp_tod,
      						'Ccont_critical':Ccont_critical,
      						'user':request.user})


      						
def cont_critical(request):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:	
      		Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
                paginator           = Paginator(Ccont_critical  , 5)
                page                = request.GET.get('page')
      try:
           Ccont_critical = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            Ccont_critical = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
           Ccont_critical = paginator.page(paginator.num_pages)
      expired_cert        =  Certificate.objects.filter(Expiringdate__lt   = date.today())
      cert_expiring_today =  Certificate.objects.filter(Expiringdate     = date.today())
      cert_critical       =  Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      crews 	          = Crew_detail.objects.all()
      Cxp_tod             = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
      xp_tod              =  Crew_Certification.objects.filter(expire_date = date.today())	
      return render_to_response('portal/crew_contXp.html',
      						{'cert_critical':cert_critical,   						
      						'cert_expiring_today':cert_expiring_today,
      						'expired_cert':expired_cert,'crews':crews,
      						'xp_tod':xp_tod,
      						'Cxp_tod':Cxp_tod,
      						'Ccont_critical':Ccont_critical,
      						'user':request.user})


def crew_cont_detail(request, id, showDetails=False):
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	else:	
    		
    		creW_cont           = crew_contract.objects.filter(pk=id)
		creW                = Crew_detail.objects.get(KrewCont__ID = id)	
    		cont_detail         = Contract_file.objects.filter(contract = creW_cont)
    		
    		
      		cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
      		cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      		#krew              = Crew_detail.objects.get( )
      		return render_to_response('portal/crew_cont_detail.html',
      						{'cert_critical':cert_critical,
      						
      						'creW':creW,
      						'cont_detail': cont_detail,
      						'creW_cont':creW_cont,
      						'cert_expiring_today':cert_expiring_today,
      						'user':request.user})







def crew_cert_detail(request, id, showDetails=False):
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	else:	
    		creW                = Crew_detail.objects.get(CREW__module_number=id)
    		creW_cert           = Crew_Certification.objects.filter(pk=id)
    		cert_detail         = Crew_Cert_file.objects.filter(certificate = creW_cert)
    		
    		
      		cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
      		cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      		
      		return render_to_response('portal/crew_cert_detail.html',
      						{'cert_critical':cert_critical,
      						
      						'creW':creW,
      						'cert_detail': cert_detail,
      						'creW_cert':creW_cert,
      						'cert_expiring_today':cert_expiring_today,


      						'user':request.user})




#CERTIFICATE VIEW- STEPHEN
def cert(request):
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       #try:
            #users_in_group = Group.objects.get(name="certificate").user_set.all()
            
            #if request.user  in users_in_group or request.user.is_superuser == True:  
       cert       = Certificate.objects.all()
       paginator  = Paginator(cert, 5)
       page       = request.GET.get('page')
       try:
       	   cert = paginator.page(page)
       except PageNotAnInteger:
		# If page is not an integer, deliver first page.
	   cert = paginator.page(1)
       except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
	   cert = paginator.page(paginator.num_pages)
       kert      		= Certificate.objects.all()
       expired_cert        	= Certificate.objects.filter(Expiringdate__lt = date.today())
       cert_expiring_today	= Certificate.objects.filter(Expiringdate = date.today())
       cert_critical 		= Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       return  render_to_response('portal/certificate.html',		 
	       						{'cert_critical':cert_critical,
	       						'user':request.user,
	       						'expired_cert':expired_cert,
	       						'cert_expiring_today':cert_expiring_today,
	       						'kert':kert,
	       						'cert':cert})
	    #else:
	         #return HttpResponseForbidden("Forbidden!!, admin You don't have access to this page!!")
     
        
       
       #except Group.DoesNotExist:	
		#return HttpResponseForbidden("Forbidden!!, ad You don't have access to this page!!")
      
def cert_search(request,term):
	galore = ''
        if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
		
	else:
		if request.GET.get('search_item','') != '':
			term = request.GET.get('search_item','')
			galore = str(term)
	       		cert = Certificate.objects.filter(document_name__icontains=term)
	       		nCert = cert
	       		paginator = Paginator(cert, 5)
		        page = request.GET.get('page')
		       
		        
	        else: 
	        	nCert = Certificate.objects.filter(document_name__icontains=galore)|Certificate.objects.filter(certificate_code__icontains=galore)
	      		paginator = Paginator(nCert, 5)
		        page = request.GET.get('page')
		        cert = nCert
	      		
        
    	try:
            cert = paginator.page(page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            cert = paginator.page(1)
        except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
            cert = paginator.page(paginator.num_pages)
        cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
        cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
        Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
        Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
        expired_cert        	= Certificate.objects.filter(Expiringdate__lt = date.today())
        certs 			= Certificate.objects.all()
	return render_to_response('portal/certSearch.html',{'cert_critical':cert_critical,
					'cert_expiring_today':cert_expiring_today,
					'cert':cert,'nCert':nCert,'certs':certs,'expired_cert':expired_cert,
					'term':term,
					'Cxp_tod':Cxp_tod,
        				'Ccont_critical':Ccont_critical,
					'user':request.user})











def cert_detail(request, id, showDetails=False):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:	
    		cert                = Certificate.objects.get(pk=id)
    		cert_file           = Cert_file.objects.filter(certificate = cert)
    		expired_cert        = Certificate.objects.filter(Expiringdate__lt = date.today())
      		cert_expiring_today = Certificate.objects.filter( Expiringdate = date.today())
      		cert_critical = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      		return render_to_response('portal/cert_detail.html',
      						{'cert_critical':cert_critical,
      						'cert':cert,
      						'expired_cert':expired_cert,
      						'cert_file':cert_file,
      						'cert_expiring_today':cert_expiring_today,


      						'user':request.user})
def cert_expired(request):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:    
                expired_cerT        = Certificate.objects.filter(Expiringdate__lt   = date.today())
                paginator  = Paginator(expired_cerT, 9)
                page       = request.GET.get('page')
      try:
            expired_cerT = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            expired_cerT = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
             expired_cerT = paginator.page(paginator.num_pages)   
               
      expired_cert        = Certificate.objects.filter(Expiringdate__lt   = date.today())
      cert_expiring_today = Certificate.objects.filter(Expiringdate     = date.today())
      cert_critical       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      kert      	  = Certificate.objects.all()
      return render_to_response('portal/cert_expired.html',
      						{'cert_critical':cert_critical,   						
      						'cert_expiring_today':cert_expiring_today,
      						'expired_cert':expired_cert,'kert':kert,'expired_cerT':expired_cerT,
      						'user':request.user})
      		
      		
def cert_expiring_Today(request):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:    
                cert_expiring_todaY = Certificate.objects.filter(Expiringdate     = date.today())
                paginator  = Paginator(cert_expiring_todaY, 9)
                page       = request.GET.get('page')
      try:
            cert_expiring_todaY = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            cert_expiring_todaY = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
             cert_expiring_todaY = paginator.page(paginator.num_pages)  	
      expired_cert        = Certificate.objects.filter(Expiringdate__lt   = date.today())
      cert_expiring_today = Certificate.objects.filter(Expiringdate     = date.today())
      cert_critical       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      kert      	    = Certificate.objects.all()
      return render_to_response('portal/cert_expiring_today.html',
      						{'cert_critical':cert_critical,   						
      						'cert_expiring_today':cert_expiring_today,'cert_expiring_todaY':cert_expiring_todaY,
      						'expired_cert':expired_cert,'kert':kert,
      						'user':request.user})
      						
def cert_critical(request):
      if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
      else:    
                cert_criticaL       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
                paginator  = Paginator(cert_criticaL , 9)
                page       = request.GET.get('page')
      try:
           cert_criticaL  = paginator.page(page)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
           cert_criticaL  = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
             cert_criticaL  = paginator.page(paginator.num_pages)   
      expired_cert        = Certificate.objects.filter(Expiringdate__lt   = date.today())
      cert_expiring_today = Certificate.objects.filter(Expiringdate     = date.today())
      cert_critical       = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
      kert      	   = Certificate.objects.all()
      return render_to_response('portal/cert_critical.html',
      						{'cert_critical':cert_critical,'cert_criticaL':cert_criticaL,  						
      						'cert_expiring_today':cert_expiring_today,
      						'expired_cert':expired_cert,'kert':kert,
      						'user':request.user})
      		
        
#REQUISITION VIEW- STEPHEN
class requestForm(ModelForm):
	class Meta:
		model = Supplies_Requisition
		exclude = ['requisitioner','reason_for_required_item','department','order_state','status','date_added','date_updated']
        	fields  = ('check',)
#requisitionOrderFormset = inlineformset_factory(requestForm,Order,extra=5)

class orderForm(ModelForm):
        class Meta:
              model = Order
      	      exclude  = ["ref","date_of_order","date_added ","date_updated"]
              fields   = ('quantity','unit','item','quote')




def requisition(request):
       Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 		     = Crew_detail.objects.all()
       requisitions_tod      = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date = date.today())
       requisitions_tod_all      = Supplies_Requisition.objects.filter(order_date = date.today())
       requisitions_tod_approved    = Supplies_Requisition.objects.filter(status ="Approved",order_date = date.today())
       requisitions_week     = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date__lte = date.today(),order_date__gte = seven_days)
       requisitions_week_approved  = Supplies_Requisition.objects.filter(status ="Approved",order_date__lte = date.today(),order_date__gte = seven_days)
       requisitions_week_all       = Supplies_Requisition.objects.filter(order_date__lte = date.today(),order_date__gte = seven_days)
       requisitions_all      = Supplies_Requisition.objects.all()
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       else:
       		
       		return  render_to_response('portal/requisition.html',{'cert_critical':cert_critical,'requisitions_tod':requisitions_tod,
       								'cert_expiring_today':cert_expiring_today,
								'requisitions_week_all':requisitions_week_all,
								'requisitions_tod_approved':requisitions_tod_approved,
								'requisitions_week':requisitions_week,
								'requisitions_week_approved':requisitions_week_approved,
								'requisitions_tod_all':requisitions_tod_all,
								'requisitions_all':requisitions_all,
       								'Cxp_tod':Cxp_tod ,
       								'crews':crews,
       								'Ccont_critical': Ccont_critical,
       								'user':request.user})

@csrf_exempt
def requisition_today(request):
       galore = ""
       rqst_detail = None
       order_detail = None
       request_form = None
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       try:
       	        if request.session["galore"] == "modal":
			galore = "modal"
                        request.session["galore"] = ""
			try:
				if request.session["rqst_detail"] is not None:
					rqst_detail  = request.session["rqst_detail"]
					order_detail = request.session["order_detail"]
                                        request.session["inst"] = request.session["rqst_detail"]
					request.session["rqst_detail"] = ""
					request.session["order_detail"] = ""
					

                                        
                        except KeyError:
				return  HttpResponseRedirect('/requisition/today/')
       except KeyError:
      		
		request.session["galore"] = ""		
       try:
       		if request.session["inst"] is not None:
       			request_form          =  requestForm(request.POST,instance = request.session["inst"])
       except KeyError:
	        pass	
	
       #request.session["inst"] = None
       Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 		     = Crew_detail.objects.all()
       requisitions_tod      = Supplies_Requisition.objects.filter(status = "Pending Approval",order_date = date.today())
       requisitions_tod_approved    = Supplies_Requisition.objects.filter(status ="Approved",order_date = date.today())
       requisitions_tod_all      = Supplies_Requisition.objects.filter(order_date = date.today())
       requisitions_week     = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date__lte = date.today(),order_date__gte = seven_days)
       
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       
       elif request.method == 'POST':
       		
                if request_form.is_valid():
			
			request_form.save()

       		
       return  render_to_response('portal/requisitionToday.html',			{'cert_critical':cert_critical,'requisitions_tod':requisitions_tod,'requisitions_week':requisitions_week,'galore':galore,'rqst_detail':rqst_detail,'order_detail':order_detail,
       								'cert_expiring_today':cert_expiring_today,'request_form':request_form,
       								'Cxp_tod':Cxp_tod,'requisitions_tod_approved':requisitions_tod_approved,
       								'crews':crews,'requisitions_tod_all':requisitions_tod_all,
       								'Ccont_critical': Ccont_critical,
       								'user':request.user})






@csrf_exempt
def request_detail(request,id, showDetails=False):

       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       Cxp_tod               = Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 		     = Crew_detail.objects.all()
       requisitions_tod      = Supplies_Requisition.objects.filter(order_date = date.today())
       requisitions_to      = Supplies_Requisition.objects.get(pk = id,order_date = date.today())
       order                 = Order.objects.filter(date_of_order = requisitions_to)
       
       
       
       request.session["galore"] = "modal"
       request.session["rqst_detail"] = requisitions_to
       request.session["order_detail"] = order
       #request.session["request_form"] = requestForm()
       
       if request.user.username == '' or request.user.is_active == False:
      		return HttpResponseRedirect('/')
       else:
       		
       		return  HttpResponseRedirect('/requisition/today/')


#requisition-today-approved
def requisition_tod_approved(request):
	stephenTA = ""
        rqst_detail_tod_approved = None
       	order_detail_tod_approved = None
        day = ""
        
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')      
        
	try:
       	        if request.session["stephenTA"] == "modal":
			stephenTA = "modal"
                        request.session["stephenTA"] = ""
			try:
				if request.session["rqst_detail_tod_approved"] is not None:
					rqst_detail_tod_approved  = request.session["rqst_detail_tod_approved"]
					order_detail_tod_approved = request.session["order_detail_tod_approved"]
                                        day = request.session["day"] 
					request.session["rqst_detail_tod_approved"] = ""
					request.session["order_detail_tod_approved"] = ""
					request.session["day"] = ""

			except KeyError:
				return  HttpResponseRedirect('/requisition/today/approved')
       	except KeyError:
      		
		request.session["stephenTA"] = ""		

        Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
       	cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       	cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       	Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       	crews 		      = Crew_detail.objects.all()
       	requisitions_tod      = Supplies_Requisition.objects.filter(status = "Pending Approval",order_date = date.today())
	requisitions_tod_all      = Supplies_Requisition.objects.filter(order_date = date.today())
       	requisitions_week     = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date__lte = date.today(),order_date__gte = seven_days)
        requisitions_tod_approved    = Supplies_Requisition.objects.filter(status ="Approved",order_date = date.today())
	
	
	return  render_to_response('portal/requisitionTodayApp.html',
							{'cert_critical':cert_critical,'requisitions_tod':requisitions_tod,
								'requisitions_week':requisitions_week,
								'stephenTA':stephenTA,'requisitions_tod_all':requisitions_tod_all,
								'rqst_detail_tod_approved':rqst_detail_tod_approved,
								'order_detail_tod_approved':order_detail_tod_approved,
       								'cert_expiring_today':cert_expiring_today,
       								'Cxp_tod':Cxp_tod,'day':day,
								'requisitions_tod_approved':requisitions_tod_approved,
       								'crews':crews,
       								'Ccont_critical': Ccont_critical,
       								'user':request.user})

@csrf_exempt
def request_detail_Approved_tod(request,id, showDetails=False):
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	Cxp_tod               	= Crew_Certification.objects.filter(expire_date = date.today())
       	cert_expiring_today   	= Certificate.objects.filter( Expiringdate = date.today())
       	cert_critical         	= Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       	Ccont_critical        	= crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       	crews 		     	= Crew_detail.objects.all()
       	
       	requisitions_tod_approved    = Supplies_Requisition.objects.get(pk = id)
       	order                 	     = Order.objects.filter(date_of_order = requisitions_tod_approved)
	day                          = requisitions_tod_approved.date_added.strftime("%A")
	
	request.session["stephenTA"] = "modal"
       	request.session["rqst_detail_tod_approved"] = requisitions_tod_approved
       	request.session["order_detail_tod_approved"] = order
        request.session["day"] = day
	if request.user.username == '' or request.user.is_active == False:
      		return HttpResponseRedirect('/')
       	else:
       		
       		return  HttpResponseRedirect('/requisition/today/approved/')



def request_print(request,id, showDetails=False):
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	
       	
       	requisitions_tod_approved    = Supplies_Requisition.objects.get(pk = id)
       	order                 	     = Order.objects.filter(date_of_order = requisitions_tod_approved)
	day                          = requisitions_tod_approved.date_added.strftime("%A")


	return  render_to_response('portal/requisitionTodayPrint.html',
							{'requisitions_tod_approved':requisitions_tod_approved,
								'order':order,'day':day,
       								'user':request.user})




def requisition_tod_all(request):
	stephen_TA = ""
        rqst_detail_tod_all = None
       	order_detail_tod_all = None
        daY = ""

	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	
	try:
       	        if request.session["stephen_TA"] == "modal":
			stephen_TA = "modal"
                        request.session["stephen_TA"] = ""
			try:
				if request.session["rqst_detail_tod_all"] is not None:
					rqst_detail_tod_all  = request.session["rqst_detail_tod_all"]
					order_detail_tod_all = request.session["order_detail_tod_all"]
                                        daY = request.session["daY"] 
					request.session["rqst_detail_tod_all"] = ""
					request.session["order_detail_tod_all"] = ""
					request.session["daY"] = ""

			except KeyError:
				return  HttpResponseRedirect('/requisition/today/all/')
       	except KeyError:
      		
		request.session["stephen_TA"] = ""
       	Cxp_tod               	= Crew_Certification.objects.filter(expire_date = date.today())
       	cert_expiring_today   	= Certificate.objects.filter( Expiringdate = date.today())
       	cert_critical         	= Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       	Ccont_critical        	= crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       	crews 		     	= Crew_detail.objects.all()
       	
       	#requisitions_tod_all    = Supplies_Requisition.objects.all()
       	#order                 	     = Order.objects.filter(date_of_order = requisitions_tod_all)
	#day                          = requisitions_tod_all.date_added.strftime("%A")
       	requisitions_tod      = Supplies_Requisition.objects.filter(status = "Pending Approval",order_date = date.today())
	requisitions_tod_all      = Supplies_Requisition.objects.filter(order_date = date.today())
       	requisitions_week     = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date__lte = date.today(),order_date__gte = seven_days)
        requisitions_tod_approved    = Supplies_Requisition.objects.filter(status ="Approved",order_date = date.today())

	return  render_to_response('portal/requisitionTodayAll.html',
							{'requisitions_tod_all':requisitions_tod_all,
							 'requisitions_tod':requisitions_tod,'cert_expiring_today':cert_expiring_today,
							 'requisitions_week':requisitions_week,'Cxp_tod':Cxp_tod,
			                                 'requisitions_tod_approved':requisitions_tod_approved,
							 'rqst_detail_tod_all':rqst_detail_tod_all,
							 'order_detail_tod_all':order_detail_tod_all,
							 'cert_critical':cert_critical,
							 'Ccont_critical':Ccont_critical,'daY':daY,
							 'crews':crews,'stephen_TA':stephen_TA,
       							 'user':request.user})


@csrf_exempt
def request_tod_all(request,id, showDetails=False):
	if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
	Cxp_tod               	= Crew_Certification.objects.filter(expire_date = date.today())
       	cert_expiring_today   	= Certificate.objects.filter( Expiringdate = date.today())
       	cert_critical         	= Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       	Ccont_critical        	= crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       	crews 		     	= Crew_detail.objects.all()
       	
       	requisitions_tod_all    = Supplies_Requisition.objects.get(pk = id)
       	order                 	     = Order.objects.filter(date_of_order = requisitions_tod_all)
	daY                          = requisitions_tod_all.date_added.strftime("%A")
	
	request.session["stephen_TA"] = "modal"
       	request.session["rqst_detail_tod_all"] = requisitions_tod_all
       	request.session["order_detail_tod_all"] = order
        request.session["daY"] = daY
	if request.user.username == '' or request.user.is_active == False:
      		return HttpResponseRedirect('/')
       	else:
       		
       		return  HttpResponseRedirect('/requisition/today/all/')



@csrf_exempt
def requisition_week(request):
		stephen = ""
      		week_rqst_detail = None
       		week_order_detail = None
       		wk_request_form = None		


		if request.user.username == '' and request.user.is_superuser == False:
      			return HttpResponseRedirect('/')


		try:
	       	        if request.session["stephen"] == "modal":
				stephen = "modal"
		                request.session["stephen"] = ""
				try:
					if request.session["week_rqst_detail"] is not None:
						week_rqst_detail  = request.session["week_rqst_detail"]
						week_order_detail = request.session["week_order_detail"]
		                                request.session["wk_inst"] = request.session["week_rqst_detail"]
						request.session["week_rqst_detail"] = ""
						request.session["week_order_detail"] = ""
					

		                                
		                except KeyError:
					return  HttpResponseRedirect('/requisition/week/')
       		except KeyError:
      		
			request.session["stephen"] = ""			

                try:
	       		if request.session["wk_inst"] is not None:
	       			wk_request_form       =  requestForm(request.POST,instance = request.session["wk_inst"])
	       	except KeyError:
			pass



		Cxp_tod               = Crew_Certification.objects.filter(expire_date = date.today())
       		cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       		cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       		Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       		crews 		     = Crew_detail.objects.all()
                requisitions_tod      = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date = date.today())
		requisitions_week     = Supplies_Requisition.objects.filter(status ="Pending Approval",order_date__lte = date.today(),order_date__gte = seven_days)
		requisitions_tod_all      = Supplies_Requisition.objects.filter(order_date = date.today())
		requisitions_tod_approved    = Supplies_Requisition.objects.filter(status ="Approved",order_date = date.today())
		if request.user.username == '' and request.user.is_superuser == False:
	      		return HttpResponseRedirect('/')
	       
	       	elif request.method == 'POST':
	       		
		        if wk_request_form.is_valid():
			
				wk_request_form.save()    



	        return  render_to_response('portal/requisitionWeek.html',{'cert_critical':cert_critical,
									'requisitions_week':requisitions_week,
									'stephen':stephen,'wk_request_form':wk_request_form,
									'week_order_detail':week_order_detail,
       									'cert_expiring_today':cert_expiring_today,
									'requisitions_tod':requisitions_tod,
       									'Cxp_tod':Cxp_tod,'week_rqst_detail':week_rqst_detail,
       									'crews':crews,
									'requisitions_tod_all':requisitions_tod_all,
									'requisitions_tod_approved':requisitions_tod_approved,
       									'Ccont_critical': Ccont_critical,
       									'user':request.user})

@csrf_exempt
def Week_request_detail(request,id, showDetails=False):

       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       Cxp_tod               = Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 		     = Crew_detail.objects.all()
       requisitions_tod      = Supplies_Requisition.objects.filter(order_date = date.today())
       requisitions_week     = Supplies_Requisition.objects.get(pk = id)
       order                 = Order.objects.filter(date_of_order = requisitions_week)
       
       
       
       request.session["stephen"] = "modal"
       request.session["week_rqst_detail"] = requisitions_week
       request.session["week_order_detail"] = order
       #request.session["request_form"] = requestForm()
       
       if request.user.username == '' or request.user.is_active == False:
      		return HttpResponseRedirect('/')
       else:
       		
       		return  HttpResponseRedirect('/requisition/week/')





        
@csrf_exempt
def add_request(request):
       if request.user.username == '' and request.user.is_superuser == False:
      		return HttpResponseRedirect('/')
       formRequest  = requestForm()
       formOrder    = orderForm()
       Cxp_tod               =  Crew_Certification.objects.filter(expire_date = date.today())
       cert_expiring_today   = Certificate.objects.filter( Expiringdate = date.today())
       cert_critical         = Certificate.objects.filter(Expiringdate__lte = two_months,Expiringdate__gt = datetime.datetime.now())
       Ccont_critical        = crew_contract.objects.filter( valid_until__lte = two_months,valid_until__gt = datetime.datetime.now())
       crews 		     = Crew_detail.objects.all()
       if request.user.username == '' or request.user.is_active == False:
      		return HttpResponseRedirect('/')
       else:
       	   # form = requestForm(request.POST)
       	    #form2 = form.save(commit=False)
           # order_set = inlineformset_factory(instance = form, Order)
       	    	
       	    if request.method == 'POST':
       		      formRequest = requestForm()
                      formOrder   = orderForm()
       		      if formRequest.is_valid() and formOrder.is_valid() :
       		      	     formRequest.save()
                             formOrder.save()
            return  render_to_response('portal/add_request.html',{'formRequest':formRequest,'formOrder':formOrder,'cert_critical':cert_critical,
       								'cert_expiring_today':cert_expiring_today ,
       								'Cxp_tod':Cxp_tod ,
       								'crews':crews,
       								'Ccont_critical': Ccont_critical,
       								'user':request.user})           		
      		
