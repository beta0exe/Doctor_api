from rest_framework import  serializers
from django.contrib.auth.models import User

from api.models import Doctor, Patient, Booking


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id","name","specialty","available_slots")
        read_only_fields = ("id",)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id","name","phone_number")
        read_only_fields = ("id",)


class BookingSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    class Meta:
        model = Booking
        fields = ("id","doctor","date","time_slots","status","patient")
        read_only_fields = ("id","status","patient")

    def validate(self, attrs):
        doctor = attrs["doctor"]
        date = attrs["date"]
        time = attrs["time_slots"]

        available_slots = doctor.available_slots
        check_slots = False
        for slot in available_slots:
            if date not in slot["day"] and time not in slot["slots"]:
                check_slots = True
                break
        if not check_slots:
            raise serializers.ValidationError("The requested time slot is not available for this doctor.")

        if Booking.objects.filter(doctor=doctor, date=date, time_slots=time).exists():
            raise serializers.ValidationError("The requested time slot is not available for this patient.")
        return attrs

