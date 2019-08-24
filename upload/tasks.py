from __future__ import absolute_import, unicode_literals
from datetime import datetime

from celery import shared_task, current_task

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from .models import Ride


@shared_task
def add_entries(data):
    quesryset = list()

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
        
            quesryset.append(
                    Ride(
                    id = row[0],
                    user_id = row[1],
                    vehicle_model_id = row[2],
                    package_id = row[3],
                    travel_type_id = row[4],
                    from_area_id = row[5],
                    to_area_id = row[6],
                    from_city_id = row[7],
                    to_city_id = row[8],
                    from_date = row[9],
                    to_date = row[10],
                    online_booking = row[11],
                    mobile_site_booking = row[12],
                    booking_created = row[13],
                    from_lat = row[14],
                    from_long = row[15],
                    to_lat = row[16],
                    to_long = row[17],
                    car_cancellation = row[18]
                )
            )

        except IndexError:
            pass

        # except:
        #     current_task.update_state(state='FAILURE')
        #     return 'Could not save in the database. Please try again.'

    try:
        Ride.objects.bulk_create(quesryset)
        return "Data saved successfully."

    except:
        current_task.update_state(state='FAILURE')
        return "'id' already exists. Flush the DB to test with same data."