from django.db import models

# Create your models here.

class Ride(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    vehicle_model_id = models.IntegerField()
    package_id = models.IntegerField(null=True, blank=True)
    travel_type_id = models.IntegerField()
    from_area_id = models.IntegerField(null=True, blank=True)
    to_area_id = models.IntegerField(null=True, blank=True)
    from_city_id = models.IntegerField(null=True, blank=True)
    to_city_id = models.IntegerField(null=True, blank=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField(null=True, blank=True)
    online_booking = models.IntegerField()
    mobile_site_booking = models.IntegerField()
    booking_created = models.DateTimeField()
    from_lat = models.FloatField(null=True, blank=True)
    from_long = models.FloatField(null=True, blank=True)
    to_lat = models.FloatField(null=True, blank=True)
    to_long = models.FloatField(null=True, blank=True)
    car_cancellation = models.IntegerField()

    def __str__(self):
        return "Ride ID: %d\tUser ID: %d" %(self.id, self.user_id)