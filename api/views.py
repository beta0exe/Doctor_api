from django.shortcuts import render
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from pyexpat.errors import messages
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from api.models import Doctor, Booking, Patient
from api.serializer import DoctorSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.sms import smssender
from django.utils.decorators import method_decorator
from django.core.cache import  cache
from time import  sleep


# Create your views here.


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Doctor.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise  serializer.validationError({"error":"User must to be authenticated"})
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({"success":True,"Message":"Doctor Profile Created","data":serializer.data},
                                status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"success":False,"Message":str("Invalid user ID or missing data.")},)


    def destroy(self, request, *args, **kwargs):
        try:
            doctor = self.get_object()
            if doctor.user_id != self.request.user.pk:
                return Response({"success":False,"Message":"User must to be authenticated"},)
            doctor.delete()
            return Response({"success":True,"message":"User Has been deleted."},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"success":False,"Message":str(e)},status=status.HTTP_400_BAD_REQUEST)



class BookingviewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cache_key = f"booking_list_{self.request.user.id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        queryset = Booking.objects.all()
        serialized_data = BookingSerializer(queryset, many=True).data
        cache.set(cache_key, serialized_data, timeout=40)
        return queryset


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        try:
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"success": False, "message": "User must be a registered patient."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.data["patient"] = patient.id
        patient_name = patient.name
        phone_number = patient.phone_number
        time_slot = request.data.get("time_slots")
        if not time_slot:
            return Response(
                {"success": False, "message": "No time slot provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        doctor_id = request.data.get("doctor")
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response(
                {"success": False, "message": "Doctor does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        booking = serializer.save(status="Confirmed")




        for slot in doctor.available_slots:
            if time_slot in slot["slots"]:
                 day_slot = slot["day"]
                 slot["slots"].remove(time_slot)
                 doctor.save()
                 break
        else:
            return Response(
                {"success": False, "message": "The selected time slot is not available."},
                status=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        print(phone_number)
        sms_sent = smssender(DAY=day_slot,NAME=patient_name,PHONE_NUMBER=phone_number)
        if not sms_sent:
            print("Somthing went wrong")
        return Response(
            {"success": True, "message": "Booking Confirmed!", "data": serializer.data},
            status=status.HTTP_201_CREATED, headers=headers
        )
