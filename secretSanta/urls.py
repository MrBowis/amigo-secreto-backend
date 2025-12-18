from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecretSantaEventViewSet

router = DefaultRouter()
router.register(r'events', SecretSantaEventViewSet, basename='secretsanta-event')

urlpatterns = router.urls
