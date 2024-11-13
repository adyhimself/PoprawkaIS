from django.test import TestCase
from django.urls import reverse
from .models import Event
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError

MAX_LINK_LENGTH = Event._meta.get_field('trainer_link').max_length or 2000
ALLOWED_ACTIONS = {'view', 'edit', 'add'}


class TrackingIntegrationTests(TestCase):
    def test_log_event_creation_and_retrieval(self):
        print("Testuje tworzenie i pobieranie logu zdarzenia.")
        response_post = self.client.post(reverse('tracking_event'), {
            'ip': '192.168.0.1', 'action_type': 'edit', 'trainer_id': 1, 'trainer_link': 'http://example.com',
            'timestamp': '2024-11-08T13:00:00Z'
        }, content_type='application/json')
        self.assertEqual(response_post.status_code, 201)

        response_get = self.client.get(reverse('tracking_logs'))
        self.assertEqual(response_get.status_code, 200)
        logs = response_get.json()
        self.assertTrue(any(log['action_type'] == 'edit' for log in logs))


class EventTests(TestCase):
    def setUp(self):
        print("Tworzę testowe zdarzenie.")
        self.event = Event.objects.create(
            ip="127.0.0.1",
            action_type="view",
            trainer_id=1,
            trainer_link="http://example.com",
            timestamp=make_aware(datetime(2024, 11, 8, 12, 0, 0))
        )

    def test_event_creation(self):
        print("Testuje tworzenie pojedynczego zdarzenia.")
        self.assertEqual(Event.objects.count(), 1)

    def test_event_post_endpoint(self):
        print("Testuje punkt końcowy POST dla zdarzeń.")
        response = self.client.post(reverse('tracking_event'), {
            'ip': '127.0.0.1', 'action_type': 'add', 'trainer_id': 2, 'trainer_link': 'http://example.com',
            'timestamp': '2024-11-08T12:00:00Z'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 2)

    def test_event_post_invalid_data(self):
        print("Testuje walidację punktu końcowego POST z nieprawidłowymi danymi.")
        response = self.client.post(reverse('tracking_event'), {
            'ip': '127.0.0.1', 'action_type': 'add', 'trainer_id': 'invalid_id'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_event_string_representation(self):
        print("Testuje reprezentację tekstową zdarzenia.")
        self.assertEqual(str(self.event), "view at 2024-11-08 12:00:00+00:00")

    def test_invalid_action_type(self):
        print("Testuje walidację dla nieprawidłowego typu akcji.")
        with self.assertRaises(ValidationError) as context:
            Event.objects.create(
                ip="127.0.0.1",
                action_type="invalid_action",
                trainer_id=1,
                trainer_link="http://example.com",
                timestamp=make_aware(datetime(2024, 11, 8, 12, 0, 0))
            )
        self.assertIn('Nieprawidłowy typ akcji.', str(context.exception))

    def test_logs_get_endpoint(self):
        print("Testuje punkt końcowy GET dla logów.")
        response = self.client.get(reverse('tracking_logs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) <= 20)

    def test_long_trainer_link(self):
        print("Testuje obsługę długiego linku do trenera.")
        long_link = 'http://' + 'a' * (MAX_LINK_LENGTH - 10) + '.com'
        response = self.client.post(reverse('tracking_event'), {
            'ip': '127.0.0.1', 'action_type': 'view', 'trainer_id': 1, 'trainer_link': long_link,
            'timestamp': '2024-11-08T12:00:00Z'
        }, content_type='application/json')
        if len(long_link) <= MAX_LINK_LENGTH:
            self.assertEqual(response.status_code, 201, "Oczekiwany kod 201 dla linku poniżej limitu znaków")
        else:
            self.assertEqual(response.status_code, 400, "Oczekiwany kod 400 dla linku powyżej limitu znaków")

    def test_filter_logs_by_date(self):
        print("Testuje filtrowanie logów według daty.")
        Event.objects.create(
            ip="127.0.0.2",
            action_type="add",
            trainer_id=2,
            trainer_link="http://example2.com",
            timestamp=make_aware(datetime(2024, 11, 9, 15, 0, 0))
        )
        start_date = '2024-11-08'
        end_date = '2024-11-09'
        response = self.client.get(reverse('tracking_logs'), {
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertEqual(response.status_code, 200)
        logs = response.json()
        self.assertTrue(all(start_date <= log['timestamp'][:10] <= end_date for log in logs))
