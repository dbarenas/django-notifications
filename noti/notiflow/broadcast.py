from django.conf import settings
from django.contrib import messages
from .serializers import ConsumerSerializer,NotificationSerializer, NotificationsArchiveSerializer,NotificationsSendArchiveSerializer
from .models import Consumer, Notification, NotificationsArchive

def set_info():
    queryset = Notification.objects.filter(broadcast=True)
    print queryset
    time.sleep(5)
    print "hello"
    print ":"*30
