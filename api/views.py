from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters

from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer
from .utils import create_or_update


class DogsViewSet(viewsets.ModelViewSet):
    """Performs CRUD operations on the Dog model"""

    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    @staticmethod
    def perform_create(self, serializer):
        breed = create_or_update(serializer)
        serializer.save(breed=breed[0])

    @staticmethod
    def perform_update(self, serializer):
        breed = create_or_update(serializer)
        serializer.save(breed=breed[0])


class BreedViewSet(viewsets.ModelViewSet):
    """Performs CRUD operations for the Breed model"""

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
