from datetime import datetime

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ride
from .serializers import RidesSerializer


class FlushDatabaseView(APIView):

    def get(self, request):
        Ride.objects.all().delete()
        return Response({'status':'Database flushed successfully.'})


class ListRidesView(APIView):

    def get(self, request):
        rides = Ride.objects.all()
        serializer = RidesSerializer(rides, many=True)

        return Response({"rides": serializer.data})


class FileUploadView(APIView):

    parser_class = (FileUploadParser,)

    def post(self, request):

        if 'file' not in request.data:
            raise ParseError("Empty content. Please attach a file to upload.")

        file_handler = request.data['file']

        content = file_handler.read().decode('utf-8').split('\n')

        data = [i.split(',') for i in content[1:]]

        # data = data[:5]

        for row_num, row in enumerate(data):
            for index, val in enumerate(row):

                try:

                    if index in (0,1,2,3,4,5,6,7,8,11,12,18):
                        row[index] = int(val)
                    
                    if index in (14,15,16,17):
                        row[index] = float(val)
                
                    if index in (9,10,13):

                        old_format = '%m/%d/%Y %H:%M' if '/' in val else '%m-%d-%Y %H:%M'
                        
                        row[index] = make_aware(parse_datetime(datetime.strptime(val, old_format).strftime('%Y-%m-%dT%H:%M:%S')))


                except ValueError:
                    row[index] = None

            try:
            
                record = Ride()
                record.id = row[0]
                record.user_id = row[1]
                record.vehicle_model_id = row[2]
                record.package_id = row[3]
                record.travel_type_id = row[4]
                record.from_area_id = row[5]
                record.to_area_id = row[6]
                record.from_city_id = row[7]
                record.to_city_id = row[8]
                record.from_date = row[9]
                record.to_date = row[10]
                record.online_booking = row[11]
                record.mobile_site_booking = row[12]
                record.booking_created = row[13]
                record.from_lat = row[14]
                record.from_long = row[15]
                record.to_lat = row[16]
                record.to_long = row[17]
                record.car_cancellation = row[18]
            
                record.save()

            except IndexError:
                print(row_num, row)

            except:
                print(row_num, row)
                return Response({'status':'Could not save in the database. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'status':'%s uploaded successfully.'%file_handler.name})