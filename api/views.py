from django.shortcuts import render
from django.template.context_processors import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from api.models import Doctor, Booking, Patient
from api.serializer import DoctorSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Fetch the patient associated with the authenticated user
            patient = Patient.objects.get(user=request.user)
        except Patient.DoesNotExist:
            return Response(
                {"success": False, "message": "User must be a registered patient."},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.data["patient"] = patient.id
        print(f"Request user: {request.user}")
        print(f"Patient: {patient.id},{request.data['patient']}")
        print(f"Request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        booking = serializer.save(status="Confirmed")
        headers = self.get_success_headers(serializer.data)
        return Response({"success":True,"Message":"Booking Confirmed!","data":serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
