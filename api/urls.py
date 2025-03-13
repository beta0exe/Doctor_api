
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from api.views import DoctorViewSet,BookingviewSet






router = DefaultRouter()

router.register('v1/appointments',BookingviewSet)
router.register(r"v1/doctors", DoctorViewSet)

urlpatterns = [
    path("",include(router.urls)),
]
