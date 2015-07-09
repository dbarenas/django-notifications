# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import routers, viewsets, permissions
 
from notiflow.views import ConsumerViewSet,NotificationViewSet, NotificationsArchiveViewSet
from hybridrouter import HybridRouter


# Uncomment the next two lines to enable the admin:
admin.autodiscover()
router = HybridRouter()

router.register(r'Consumer', ConsumerViewSet)
router.register(r'Notification', NotificationViewSet)

#router.add_api_view("Notification", url(r'^notification/$', NotificationViewSet.as_view(), name='notification'))
router.add_api_view("Notifications Archive", url(r'^notification_archives/$', NotificationsArchiveViewSet.as_view(), name='notification_archives'))


#Add here url for REST views
urlpatterns = patterns(
    '',
	url(r'^', include(router.urls)),
	url(r'^admin/', include(admin.site.urls)),
)
