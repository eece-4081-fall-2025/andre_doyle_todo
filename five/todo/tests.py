from django.test import TestCase
from django.urls import reverse
from .models import ToDo

class ToDoModelTest(TestCase):
    def test_str_returns_name(self):
        task = ToDo.objects.create(name="Test task")
        self.assertEqual(str(task), "Test task")

class ToDoViewTests(TestCase):
    def test_task_list_page_loads(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.post(reverse("task_create"), {"name": "New task"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDo.objects.count(), 1)

    def test_delete_task(self):
        task = ToDo.objects.create(name="Delete me")
        response = self.client.post(reverse("task_delete", args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ToDo.objects.count(), 0)

    def test_toggle_completion(self):
        task = ToDo.objects.create(name="Toggle me", complete=False)
        response = self.client.get(reverse("task_toggle", args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.complete)
