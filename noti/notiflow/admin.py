# -*- coding: utf-8 -*-

from django.contrib import admin

from django.db import models

from notiflow.models import Notification, NotificationsArchive,Consumer
from celery import Celery
from notiflow.tasks import parse_task_file,add

#-----
import logging
import sys
import os
from django.contrib.messages import get_messages
from django.contrib import messages
from django.db.models.signals import post_save
from django.core.signals import request_finished
#-----

# Get an instance of a logger

logger = logging.getLogger(__name__)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message')

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.broadcast is True:
            print "-"*10+"Enter into: parse_task_file "+("-"*10)
            parse_task_file.delay(obj.notification_id)


class NotificationArchiveAdmin(admin.ModelAdmin):
    list_display = ('consumer_id', 'viewed')

    def get_email(self, obj):
        return obj.notification_id.consumer_id
        get_email.short_description = 'Notification'

class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('consumer_id')


admin.site.register(Notification,NotificationAdmin)
admin.site.register(NotificationsArchive)
admin.site.register(Consumer)
