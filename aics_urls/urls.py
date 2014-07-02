from django.conf.urls.defaults import *
from aics_urls.views import *
from model_report import report
report.autodiscover()


urlpatterns = patterns('',
		  url(r'^$', 'aics_urls.views.do_login'),
                  url(r'^main_portal/$', 'aics_urls.views.main_portal'),
		  url(r'^aics_portal/$', 'aics_urls.views.portal'),
		 
		  url(r'^logout/$', 'aics_urls.views.do_logout'),
		  url(r'^aics/changepass/$','aics_urls.views.password_change'),
		  url(r'^aics/changedpass/$','aics_urls.views.changedpass'),
		 
		  url(r'^add_user/$', 'aics_urls.views.add_User'),
		  
		  
		  #CREW URLS
		  url(r'^crew/$', 'aics_urls.views.crew'),
		  url(r'^crew/search/(?P<term>.*?)$','aics_urls.views.crew_search'),
		  url(r'^crew/list/$', 'aics_urls.views.crew_list'),
		  url(r'^crew_details/(?P<term>.*?)/(?P<showDetails>.*?)/$', 'aics_urls.views.crew_detail'),
		  #url(r'^crew/history/$', 'aics_urls.views.crew_history'),
		  url(r'^crew/cert_expired/$', 'aics_urls.views.crew_xp'),
		  url(r'^crew/cont_critical/$', 'aics_urls.views.cont_critical'),
		  url(r'^crew/cert_details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.crew_cert_detail'),
		  url(r'^crew/cont_details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.crew_cont_detail'),
		 
		  
		  #CERTICATE URLS
		  url(r'^certificate/$', 'aics_urls.views.cert'),
		  url(r'^cert_details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.cert_detail'),
		  url(r'^certificate/cert_expired/$', 'aics_urls.views.cert_expired'),
		  url(r'^certificate/cert_expiring_today/$', 'aics_urls.views.cert_expiring_Today'),
		  url(r'^certificate/cert_critical/$', 'aics_urls.views.cert_critical'),
		  url(r'^certificate/search/(?P<term>.*?)$','aics_urls.views.cert_search'),
		  
		  #REQUISITION URLS
		  url(r'^requisition/$', 'aics_urls.views.requisition'),
		  url(r'^requisition/add/$', 'aics_urls.views.add_request'),
		  url(r'^requisition/today/$', 'aics_urls.views.requisition_today'),
		  url(r'^requisition/details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.request_detail'),
                  url(r'^requisition/today/approved/$', 'aics_urls.views.requisition_tod_approved'),
                  url(r'^requisition/today/approved/details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.request_detail_Approved_tod'),
		  url(r'^requisition/today/approved/details/print/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.request_print'),
		  url(r'^requisition/today/all/$', 'aics_urls.views.requisition_tod_all'),
                  url(r'^requisition/today/all/details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.request_tod_all'),
		  url(r'^requisition/week/$', 'aics_urls.views.requisition_week'),
     		  url(r'^requisition/week/details/(?P<id>\d+)/((?P<showDetails>.*)/)?$', 'aics_urls.views.Week_request_detail'),
		 
			
		  	
		  
		  
		 
		 
		  
)
  
