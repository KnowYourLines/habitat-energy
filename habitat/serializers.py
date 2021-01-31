from rest_framework import serializers

from habitat.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ["unique_bid_number", "accepted_or_rejected", "delivery_date"]
