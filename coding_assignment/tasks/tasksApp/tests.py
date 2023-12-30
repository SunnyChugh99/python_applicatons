from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task
from .serializers import TaskSerializer

class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_data = {'title': 'Test Task', 'description': 'This is a test task.', 'status': 'Pending'}
        self.task = Task.objects.create(**self.task_data)
        self.url_list_create = reverse('task-list-create')
        self.url_retrieve_update_destroy = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task.id})

    def test_retrieve_task_list(self):
        response = self.client.get(self.url_list_create)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        response = self.client.post(self.url_list_create, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)  # Assuming you have one existing task

    def test_retrieve_task_detail(self):
        response = self.client.get(self.url_retrieve_update_destroy)
        task = Task.objects.get(id=self.task.id)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        updated_data = {'title': 'Updated Task', 'description': 'This task has been updated.', 'status': 'Completed'}
        response = self.client.put(self.url_retrieve_update_destroy, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, updated_data['title'])
        self.assertEqual(updated_task.description, updated_data['description'])
        self.assertEqual(updated_task.status, updated_data['status'])

    def test_delete_task(self):
        response = self.client.delete(self.url_retrieve_update_destroy)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)  # Assuming you have deleted the existing task
