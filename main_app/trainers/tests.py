from django.test import TestCase
from django.urls import reverse
from .models import Trainer
from .forms import TrainerForm
from unittest.mock import patch


class IntegrationTests(TestCase):

    @patch('trainers.views.requests.post')
    def test_trainer_create_logs_event(self, mock_post):
        print("Testuje logowanie zdarzenia przy tworzeniu trenera.")
        response = self.client.post(reverse('trainer_add'), {
            'first_name': 'Jane', 'last_name': 'Doe', 'email': 'jane.doe@example.com', 'phone': '+48123456788'
        })
        self.assertTrue(mock_post.called)
        self.assertEqual(response.status_code, 302)


class TrainerTests(TestCase):

    def setUp(self):
        self.trainer = Trainer.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com", phone="+48123456789"
        )

    def test_trainer_list_view(self):
        print("Testuje widok listy trenerów.")
        response = self.client.get(reverse('trainer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainers/trainer_list.html')

    def test_trainer_create_view(self):
        print("Testuje tworzenie nowego trenera.")
        response = self.client.post(reverse('trainer_add'), {
            'first_name': 'Jane', 'last_name': 'Doe', 'email': 'jane.doe@example.com', 'phone': '+48123456788'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Trainer.objects.count(), 2)

    def test_trainer_update_view(self):
        print("Testuje aktualizację danych trenera.")
        response = self.client.post(reverse('trainer_edit', args=[self.trainer.id]), {
            'first_name': 'John', 'last_name': 'Smith', 'email': 'john.doe@example.com', 'phone': '+48123456789'
        })
        self.trainer.refresh_from_db()
        self.assertEqual(self.trainer.last_name, 'Smith')

    def test_trainer_delete_view(self):
        print("Testuje usuwanie trenera.")
        response = self.client.post(reverse('trainer_delete', args=[self.trainer.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Trainer.objects.count(), 0)

    def test_trainer_log_event_view(self):
        print("Testuje widok logów zdarzeń.")
        response = self.client.get(reverse('log_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainers/log_list.html')
        self.assertContains(response, 'Typ Akcji')
        self.assertContains(response, 'Data Akcji')

    def test_trainer_form_validation(self):
        print("Testuje walidację formularza trenera.")
        form_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'invalid-email', 'phone': '12345'}
        form = TrainerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('phone', form.errors)

    def test_trainer_create_view_invalid_data(self):
        print("Testuje tworzenie trenera z nieprawidłowymi danymi.")
        response = self.client.post(reverse('trainer_add'), {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'phone': '+48123456788'
        })
        response.client = self.client
        response.render()
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ['To pole jest wymagane.'])

    def test_trainer_update_view_invalid_data(self):
        print("Testuje aktualizację trenera z nieprawidłowymi danymi.")
        response = self.client.post(reverse('trainer_edit', args=[self.trainer.id]), {
            'first_name': 'John', 'last_name': '', 'email': 'john.doe@example.com', 'phone': '+48123456789'
        })
        response.client = self.client
        response.render()
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ['To pole jest wymagane.'])

    def test_log_list_view_limits_entries(self):
        print("Testuje ograniczenie liczby wpisów logów do 20.")
        for i in range(30):
            Trainer.objects.create(
                first_name=f"John{i}", last_name="Doe", email=f"john{i}.doe@example.com", phone=f"+4812345678{i}"
            )
        response = self.client.get(reverse('log_list'))
        logs = response.context['logs']
        self.assertTrue(len(logs) <= 20)
