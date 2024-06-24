
from django.urls import path

from .views import TrackerView

urlpatterns = [
    path('trackers/<int:number>', TrackerView.as_view()), # POST
    path('trackers/<str:task_id>', TrackerView.as_view()), # DELETE
]
