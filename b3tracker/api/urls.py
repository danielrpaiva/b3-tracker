
from django.urls import path

from .views import TrackerView, TestView

urlpatterns = [
    path('trackers/<int:number>', TrackerView.as_view()), # POST
    path('trackers/<str:task_id>', TrackerView.as_view()), # PUT
    path('tests', TestView.as_view()), # GET
]
