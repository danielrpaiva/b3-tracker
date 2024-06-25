from django.contrib import admin

from .models import TrackOrder, OrderQuote

class TrackOrders(admin.ModelAdmin):
    list_display = (
        "id", 
        "requester_email", 
        "ticker_code", 
        "frequency", 
        "buy_limit", 
        "sell_limit", 
        "is_active",
        "task_id",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "requester_email",
        "task_id",
        "ticker_code",
        "is_active",
    )
    list_display_links = (
        "id",
    )
    search_fields = (
        "id",
        "requester_email",
        "task_id",
        "ticker_code",
        "is_active",
    )
    list_per_page = 50


class OrderQuotes(admin.ModelAdmin):
    list_display = (
        "id", 
        "track_order",
        "quote_price",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "track_order",
    )
    list_display_links = (
        "id",
    )
    search_fields = (
        "id",
        "track_order",
    )
    list_per_page = 100


admin.site.register(TrackOrder, TrackOrders)
admin.site.register(OrderQuote, OrderQuotes)