from django.db import models

# Create your models here.

class Ride(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    vehicle_model_id = models.IntegerField()
    package_id = models.IntegerField()
    travel_type_id = models.IntegerField()
    from_area_id = models.IntegerField()
    to_area_id = models.IntegerField()
    from_city_id = models.IntegerField()
    to_city_id = models.IntegerField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    online_booking = models.IntegerField()
    mobile_site_booking = models.IntegerField()
    booking_created = models.DateTimeField()
    from_lat = models.FloatField()
    from_long = models.FloatField()
    to_lat = models.FloatField()
    to_long = models.FloatField()
    car_cancellation = models.IntegerField()

    def __str__(self):
        return "Ride ID: %d\tUser ID: %d" %(self.id, self.user_id)