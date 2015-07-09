from rest_framework import serializers
from django.db.models import  Max
from django.conf import settings
from rest_framework.pagination import PaginationSerializer
from rest_framework import pagination
from django.db.models import Q
from .models import Notification, NotificationsArchive, Consumer

class ConsumerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
            model = Consumer
            fields = ('consumer_id','name')    

class NotificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
            model = Notification
            fields = ('notification_id','title','message')    

class NotificationsArchiveSerializer(serializers.HyperlinkedModelSerializer):
	notification_id = NotificationSerializer(many=True, read_only=True)
	consumer_id = ConsumerSerializer(many=True, read_only=True)

	class Meta:
    		model = NotificationsArchive
    		fields = ('consumer_id', 'notification_id', 'viewed')    

class NotificationsSendArchiveSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
            model = NotificationsArchive
            fields = ('consumer_id', 'notification_id', 'viewed')    

