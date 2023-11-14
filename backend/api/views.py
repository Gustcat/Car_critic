from rest_framework import viewsets

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


class CountryViewSet(viewsets.ViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class ProducerViewSet(viewsets.ViewSet):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()


class CarViewSet(viewsets.ViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class CommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Car.comments.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(email=self.request.user.email)
        else:
            serializer.save()
