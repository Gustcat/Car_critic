from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CountryViewSet,
    ProducerViewSet,
    CarViewSet,
    CommentViewSet,
    )

app_name = 'api'

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'producers', ProducerViewSet)
router.register(r'cars', CarViewSet)
router.register(r'cars/comments',
                CommentViewSet,
                basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
