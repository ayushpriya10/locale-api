from datetime import datetime

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
       
        if request.data:
            task_id = request.data['task_id']
            task = AsyncResult(task_id)

        return Response({
            'Task State':str(task.state),
            'Task Result':str(task.result)
            })


class RideDetails(APIView):

    parser_classes = (JSONParser,)

    def post(self, request):

        try:
            
            if request.data:
                ride_id = int(request.data['ride_id'])
                ride_details = Ride.objects.filter(id=ride_id)
            else:
                return Response({"error":'Empty Content. Please enter a valid ride_id parameter.'})

            if ride_details:
                ride_details = {
                    'id':ride_details[0].id,
                    'user_id':ride_details[0].user_id,
                    'vehicle_model_id':ride_details[0].vehicle_model_id,
                    'package_id':ride_details[0].package_id,
                    'travel_type_id':ride_details[0].travel_type_id,
                    'from_area_id':ride_details[0].from_area_id,
                    'to_area_id':ride_details[0].to_area_id,
                    'from_city_id':ride_details[0].from_city_id,
                    'to_city_id':ride_details[0].to_city_id,
                    'from_date':ride_details[0].from_date,
                    'to_date':ride_details[0].to_date,
                    'online_booking':ride_details[0].online_booking,
                    'mobile_site_booking':ride_details[0].mobile_site_booking,
                    'booking_created':ride_details[0].booking_created,
                    'from_lat':ride_details[0].from_lat,
                    'from_long':ride_details[0].from_long,
                    'to_lat':ride_details[0].to_lat,
                    'to_long':ride_details[0].to_long,
                    'car_cancellation':ride_details[0].car_cancellation
                    }

                return Response({
                    'Ride Details':ride_details,
                    })
            else:
                return Response({
                    'error':'Ride with the given ID does not exist. Please check and try again.'
                })

        except ValueError:
            return Response({'error':'Cannot resolve givrm ride_id into proper type. Please provide a valid ride_id.'})