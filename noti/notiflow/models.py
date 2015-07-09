from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery import Celery
from celery.execute import *
from djcelery_model.models import TaskMixin


class Consumer(TaskMixin, models.Model):
	consumer_id = models.IntegerField(primary_key=True,editable=False,blank=True)
	name = models.CharField(max_length=256)

	def __unicode__(self):
			return str(self.consumer_id)

	def save(self, *args, **kwargs):

		if not self.consumer_id :
			no = Consumer.objects.count()
			if no == 0:
				self.consumer_id = 1
			else:
				self.consumer_id = self.__class__.objects.all().order_by("-consumer_id")[0].consumer_id + 1
		else:
			currentObject = Consumer.objects.get(consumer_id = self.consumer_id)

		super(Consumer, self).save(*args, **kwargs)


class Notification(TaskMixin, models.Model):
	notification_id = models.IntegerField(primary_key=True, editable=False, blank=True)
	title = models.CharField(max_length=256)
	message = models.TextField()
	broadcast = models.BooleanField(blank=True)

	def __unicode__(self):
			return str(self.title)

	def save(self, *args, **kwargs):

		if not self.notification_id :
			no = Notification.objects.count()
			if no == 0:
				self.notification_id = 1
			else:
				self.notification_id = self.__class__.objects.all().order_by("-notification_id")[0].notification_id + 1
		else:
			currentObject = Notification.objects.get(notification_id = self.notification_id)

		super(Notification, self).save(*args, **kwargs)


class NotificationsArchive(TaskMixin, models.Model):
	consumer_id = models.ForeignKey(Consumer, related_name='notification_consumer')
	notification_id = models.ForeignKey(Notification, related_name='notification')
	viewed = models.BooleanField(blank=True)

	def __unicode__(self):
		return u'%s : %s - viewed : %s' % (self.consumer_id, self.notification_id, self.viewed)

class NotificationsUserPowerSegment(models.Model):
    segment_id = models.IntegerField(primary_key=True, editable=False, blank=True)
    consumer_id = models.IntegerField(editable=False, blank=False)
    power_id = models.IntegerField(editable=False, blank=False)
    power_startdate = models.IntegerField(editable=False, blank=False)
    power_closedate = models.IntegerField(editable=False, blank=False)
    power_update_at = models.IntegerField(editable=False, blank=False)

    def __unicode__(self):
        return self.segment_id

