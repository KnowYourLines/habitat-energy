from rest_framework import mixins, viewsets

from habitat.serializers import RecordSerializer
from habitat.services import get_habitat_records


class RecordsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_habitat_records()
    serializer_class = RecordSerializer
