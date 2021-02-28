from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DogsViewSet, BreedViewSet

router = DefaultRouter()

router.register("dogs", DogsViewSet, basename="dogs")
router.register("breeds", BreedViewSet, basename="breeds")

urlpatterns = [path("", include(router.urls))]
