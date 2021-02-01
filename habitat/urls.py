from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habitat import views

router = DefaultRouter()
router.register(r"daily_records", views.RecordsViewSet, basename="daily_records")

urlpatterns = [
    path("", include(router.urls)),
]
