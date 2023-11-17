from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from cars.models import (
    Country,
    Producer,
    Car,
    )
from .serializers import (
    CountrySerializer,
    CarSerializer,
    ProducerSerializer,
    CommentSerializer,
    )
from .permissions import (
    AuthenticatedOrReadOnly,
    AuthorOrCreateOrReadOnly
)
from .utilities import load_xlsx, load_csv


class ListDownloadViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        result = super().list(request)
        if request.GET.get('format') == 'xlsx':
            return load_xlsx(result.data)
        elif request.GET.get('format') == 'csv':
            return load_csv(result.data)
        return result


class CountryViewSet(ListDownloadViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [AuthenticatedOrReadOnly]


class ProducerViewSet(ListDownloadViewSet):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()
    permission_classes = [AuthenticatedOrReadOnly]


class CarViewSet(ListDownloadViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [AuthenticatedOrReadOnly]


class CommentViewSet(ListDownloadViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrCreateOrReadOnly]

    def get_queryset(self):
        car = get_object_or_404(Car, id=self.kwargs.get('car_id'))
        return car.comments.all()
