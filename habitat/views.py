from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from habitat.models import Record
from habitat.serializers import RecordSerializer
from habitat.services import get_habitat_records


class RecordsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    @action(detail=False, methods=["get"])
    def cache(self, request):
        queryset = get_habitat_records()
        result = self.get_serializer(queryset, many=True)
        return Response(result.data)
