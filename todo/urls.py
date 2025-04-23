from django.urls import path
from .views import TaskListCreateView, TaskDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Перенесли сюда
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Перенесли сюда
]