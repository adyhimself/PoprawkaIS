from django.urls import path
from .views import EventView, LogsView

urlpatterns = [
    path('event/', EventView.as_view(), name='tracking_event'),
    path('logs/', LogsView.as_view(), name='tracking_logs'),
]
