from rest_framework import  serializers

from api.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id","name","speciality","available_slots")
        read_only_fields = ("id",)