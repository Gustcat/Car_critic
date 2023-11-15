from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from cars.models import (
    Country,
    Producer,
    Car,
    Comment,
    )
from .serializers import (
    CountrySerializer,
    CarSerializer,
    ProducerSerializer,
    CommentSerializer,
    )


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class ProducerViewSet(viewsets.ModelViewSet):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        car_id = self.kwargs.get('car_id')
        car = get_object_or_404(Car, id=car_id)
        return car.comments.all()

    # def perform_create(self, serializer):
    #     if self.request.user.is_authenticated:
    #         serializer.save(email=self.request.user.email)
    #     else:
    #         serializer.save()
