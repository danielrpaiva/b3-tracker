
from django.urls import path

from .views import TrackerView, TaskDebugView, TickerView

urlpatterns = [
    path('trackers', TrackerView.as_view()), # POST, GET
    path('trackers/<str:task_id>', TrackerView.as_view()), # PUT
    path('tickers', TickerView.as_view()), # GET
    path('tasks-debug', TaskDebugView.as_view()), # GET
]
