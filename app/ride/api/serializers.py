from rest_framework import serializers
from django.utils.timezone import now, timedelta

from ride.models import *

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id', 'description', 'created_at']

class RideSerializer(serializers.ModelSerializer):
    todays_ride_events = serializers.SerializerMethodField()
    rider_email = serializers.EmailField(source='rider.email')
    driver_email = serializers.EmailField(source='driver.email')

    class Meta:
        model = Ride
        fields = [
            'id', 'status', 'rider', 'rider_email', 'driver', 'driver_email',
            'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 
            'dropoff_longitude', 'pickup_time', 'todays_ride_events'
        ]

    def get_todays_ride_events(self, obj):
        last_24_hours = now() - timedelta(hours=24)
        events = obj.events.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(events, many=True).data
