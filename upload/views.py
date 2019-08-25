from datetime import datetime
from itertools import islice

from celery.result import AsyncResult
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ride
from .serializers import RidesSerializer
from .tasks import add_entries


class FlushDatabaseView(APIView):

    def get(self, request):
        Ride.objects.all().delete()

        return Response({'status':'Database flushed successfully.'})


class ListRidesView(APIView):

    def get(self, request):
        rides = Ride.objects.all()
        serializer = RidesSerializer(rides, many=True)

        return Response({"rides": serializer.data})


class AsyncFileHandler(APIView):

    parser_class = (FileUploadParser,)

    def post(self, request):

        if 'file' not in request.data:
            raise ParseError("Empty content. Please attach a file to upload.")

        file_handler = request.data['file']

        content = file_handler.read().decode('utf-8').split('\n')

        data = [i.split(',') for i in content[1:]]

        task_id = add_entries.delay(data)

        return Response({
            'status':'%s uploaded successfully.'%file_handler.name,
            'Task ID':str(task_id)
            })


class TaskStatus(APIView):

    parser_classes = (JSONParser,)

    def post(self, request):
        data = 'Fail'
        
        if request.data:
            task_id = request.data['task_id']
            print(task_id)
            task = AsyncResult(task_id)
        else:
            data = 'No task_id in the request'

        return Response({
            'Task State':str(task.state),
            'Task Result':str(task.result)
            })