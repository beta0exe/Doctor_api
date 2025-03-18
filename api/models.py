from django.contrib.auth.models import User
from django.db import models
from django.views.debug import default_urlconf


# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    available_slots = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Booking(models.Model):

    status_pending = "Pending"
    status_Confirmed = "Confirmed"
    status_Failed = "Failed"
    status_choices = [
        (status_pending,"pending"),
        (status_Confirmed,"Confirmed"),
        (status_Failed,"Failed"),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    time_slots = models.CharField(max_length=20)
    status = models.CharField(max_length=20,choices=status_choices,default=status_pending)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

