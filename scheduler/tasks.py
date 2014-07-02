from celery import task

from certificate.models import *
from celery.decorators import periodic_task
from datetime import timedelta
from celery.task.schedules import crontab
import datetime
from datetime import date
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import Context, loader

def expired_cert():
    cert = Certificate.objects.filter(Expiringdate__lte = date.today())
    for c in cert:
        print c
    return HttpResponseRedirect('portal/mainpage.html')
      
@periodic_task(run_every=crontab(hour="*",minute="*/1",day_of_week="*"))
def add():
    expired_cert()
    print "it works"
    

