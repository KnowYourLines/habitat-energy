from rest_framework import mixins, viewsets
from habitat.serializers import RecordSerializer
from habitat.services import get_habitat_records


class RecordsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RecordSerializer

    def get_queryset(self):
        return get_habitat_records()
