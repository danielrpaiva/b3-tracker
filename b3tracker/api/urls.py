
from django.urls import path

from .views import TrackerView, TaskDebugView

urlpatterns = [
    path('trackers', TrackerView.as_view()), # POST
    path('trackers/<str:task_id>', TrackerView.as_view()), # PUT
    path('tasks-debug', TaskDebugView.as_view()), # GET
]
