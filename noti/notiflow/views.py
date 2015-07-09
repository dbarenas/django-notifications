from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated

from .serializers import ConsumerSerializer,NotificationSerializer, NotificationsArchiveSerializer,NotificationsSendArchiveSerializer
from .models import Consumer, Notification, NotificationsArchive

class ConsumerViewSet(viewsets.ModelViewSet):
	queryset = Consumer.objects.all()
	serializer_class = ConsumerSerializer

class NotificationViewSet(viewsets.ModelViewSet):
	queryset = Notification.objects.all()
	serializer_class = NotificationSerializer

class NotificationsArchiveViewSet(APIView):

	def get_object(self, pk):
		try:
			return NotificationsArchive.objects.get(pk=pk)
		except NotificationsArchive.DoesNotExist:
			raise Http404

	def get(self, request, format=None):
		query = self.request.QUERY_PARAMS

		if 'consumer_id' in query.keys():

			queryset = NotificationsArchive.objects.filter(consumer_id=query.get('consumer_id'))

			messages_dict = []

			for i in queryset:
				current_message = {}
				current_message['id'] = i.pk
				current_message['menssage'] = i.notification_id.message
				current_message['viewed'] = i.viewed
				messages_dict.append(current_message)
			# serializer = NotificationsArchiveSerializer('json', queryset, many=True, context={'request': request})
			return Response(data={'result':messages_dict}, status=status.HTTP_200_OK)
		else:
			return Response({'result':'Error'}, status=status.HTTP_400_BAD_REQUEST)


	def put(self, request, format=None):
		print "PUT"*10
		query = self.request.QUERY_PARAMS
		print query
		received = request.DATA
		if received.has_key('archive_id') and received.has_key('all_read') and received.has_key('consumer_id'):
			archive_id = request.DATA['archive_id']
			all_read = request.DATA['all_read']
			consumer_id = request.DATA['coensumer_id']
			if all_read == 0:
				print "aa"*30
				res=NotificationsArchive.objects.filter(pk=archive_id).update(viewed='TRUE')
				if res >= 1:
					return Response(data={'result':'OK'}, status=status.HTTP_201_CREATED)
			else:
				print "bb"*30
				res=NotificationsArchive.objects.filter(consumer_id=consumer_id).update(viewed='TRUE')
				if res >= 1:
					return Response(data={'result':'OK'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'result':'Error'}, status=status.HTTP_400_BAD_REQUEST)


	def post(self, request, format=None):
		error=''
		consumer_id = request.DATA['consumer_id']
		notification_id = request.DATA['notification_id']

		resTrue=NotificationsArchive.objects.filter(consumer_id=consumer_id, notification_id=notification_id,viewed=True).count()
		resSiFalse=NotificationsArchive.objects.filter(consumer_id=consumer_id, notification_id=notification_id,viewed=False).count()

		print resTrue, resSiFalse
		if resTrue >= 0 and resSiFalse+1 <= 1:

			dic = {'consumer_id' : '/consumer/'+str(consumer_id)+'/', 'notification_id' : '/notification/'+str(notification_id)+'/'}
			print dic
			serializer = NotificationsSendArchiveSerializer(data=dic, context={'request': request}, partial=True)
			print serializer.errors
			if serializer.is_valid():
				serializer.save()
				print "**"*30
			else :
				error = error +str(consumer_id) + ', '

			if error == '':
				return Response({'message':'ADD MESSSAGE OKAY'}, status=status.HTTP_201_CREATED)
			return Response({'error':'there are a error in the info = '+error}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'error':' Notification already sended'}, status=status.HTTP_400_BAD_REQUEST)

