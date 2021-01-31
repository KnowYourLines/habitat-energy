from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habitat import views

router = DefaultRouter()
router.register(r"records", views.RecordsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
