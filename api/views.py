from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from api.models import Doctor
from api.serializer import DoctorSerializer
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
