from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()

        # Получаем токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Аутентифицируем клиента
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Создаем тестовую задачу
        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            is_completed=False
        )

    def test_get_task_list(self):
        """Тест на получение списка задач"""
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Task")

    def test_create_task(self):
        """Тест на создание новой задачи"""
        url = reverse('task-list-create')
        data = {
            "title": "New Task",
            "description": "New Description",
            "is_completed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, "New Task")

    def test_get_task_detail(self):
        """Тест на получение конкретной задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Task")

    def test_update_task(self):
        """Тест на обновление задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "is_completed": True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.is_completed, True)

    def test_delete_task(self):
        """Тест на удаление задачи"""
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter_tasks_by_status(self):
        """Тест на фильтрацию задач по статусу"""
        url = reverse('task-list-create') + '?is_completed=false'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # Создаем завершенную задачу
        Task.objects.create(
            user=self.user,
            title="Completed Task",
            description="Completed Description",
            is_completed=True
        )
        url = reverse('task-list-create') + '?is_completed=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_unauthenticated_access(self):
        """Тест на доступ без аутентификации"""
        self.client.credentials()  # Убираем токен
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)