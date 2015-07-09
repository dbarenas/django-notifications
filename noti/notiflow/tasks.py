# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
from django.conf import settings

from celery import Celery


#app = Celery('tasks', broker='amqp://amqp://guest:**@localhost:5672//')

app = Celery('tasks', broker='AMQP://localhost/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'noti.settings'
reload(sys)

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
from .models import Consumer,Notification,NotificationsArchive

@app.task
def parse_task_file(notification_id):
	no = Consumer.objects.all()
	for i in no:
		print str(i.consumer_id)+"::::"+str(notification_id)
		notification = Notification.objects.get(notification_id=notification_id)
		p = NotificationsArchive.objects.create(consumer_id=i, notification_id=notification, viewed=0)

@app.task
def add():
	import time
	print "Inicia el envío del email..."
	repeats = range(3)
	for n_repeat in repeats:
		res = time.sleep(1)
		print "{0} sec.".format((n_repeat+1))
	print "email enviado a %s" % res
	 