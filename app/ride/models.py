from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now 


# Create your models here.

User = get_user_model()


class Ride(models.Model):

    STATUS_CHOICES = [
        ("en-route","en-route"),
        ("pickup","pickup"),
        ("dropoff","dropoff")

    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en-route')
    rider = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rider_rides',
        limit_choices_to={'role': 'rider'}
    )
    driver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='driver_rides',
        limit_choices_to={'role': 'driver'}
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()


    def clean(self):
        """Custom validation to ensure correct user roles."""
        if self.rider.role != 'rider':
            raise ValidationError(_('Assigned user to "id_rider" must have the "rider" role.'))

        if self.driver.role != 'driver':
            raise ValidationError(_('Assigned user to "id_driver" must have the "driver" role.'))

    def save(self, *args, **kwargs):
        """Ensure data is validated before saving."""
        self.full_clean()
        super(Ride, self).save(*args, **kwargs)

    def __str__(self):
        return f"Ride {self.id} - Rider: {self.rider.email}, Driver: {self.driver.email}"
    


class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE,related_name="events")

    description = models.TextField()  
    created_at = models.DateTimeField(default=now)


    class Meta:
        ordering = ['-created_at']  # Order events by latest first

    def __str__(self):
        """String representation of the event."""
        return f"Ride {self.ride.id}: {self.description[:30]}... ({self.created_at})"
