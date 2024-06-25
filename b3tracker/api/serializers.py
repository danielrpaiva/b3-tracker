from rest_framework import serializers
from .models import TrackOrder, OrderQuote

class TrackOrderBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackOrder
        fields = "__all__"

class OrderQuoteBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderQuote
        fields = "__all__"

class OrderQuoteCompleteSerializer(serializers.ModelSerializer):
    track_order = TrackOrderBasicSerializer()

    class Meta:
        model = OrderQuote
        fields = "__all__"


class OrderQuoteListSerializer(serializers.ModelSerializer):
    ticker_code = serializers.ReadOnlyField(source="track_order.ticker_code")
    task_id = serializers.ReadOnlyField(source="track_order.task_id")
    requester_email = serializers.ReadOnlyField(source="track_order.requester_email")

    class Meta:
        model = OrderQuote
        fields = [
            "id",
            "quote_price",
            "ticker_code",
            "task_id",
            "requester_email",
        ]