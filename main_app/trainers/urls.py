from django.urls import path
from .views import TrainerListView, TrainerCreateView, TrainerUpdateView, TrainerDeleteView, LogListView

urlpatterns = [
    path('', TrainerListView.as_view(), name='trainer_list'),
    path('add/', TrainerCreateView.as_view(), name='trainer_add'),
    path('edit/<int:pk>/', TrainerUpdateView.as_view(), name='trainer_edit'),
    path('delete/<int:pk>/', TrainerDeleteView.as_view(), name='trainer_delete'),
    path('logs/', LogListView.as_view(), name='log_list'),
]
