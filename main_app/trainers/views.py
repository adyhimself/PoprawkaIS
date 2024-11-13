from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.html import format_html
from dateutil.parser import parse
from .models import Trainer
from .forms import TrainerForm
import requests

TRACKING_URL = 'http://localhost:8001/tracking/event/'


def send_event(request, action_type, trainer=None):
    print(f"Wysyłanie eventu o typie akcji: {action_type}")
    event = {
        'ip': get_client_ip(request),
        'action_type': action_type,
        'trainer_id': trainer.id if trainer else None,
        'trainer_name': f"{trainer.first_name} {trainer.last_name}" if trainer else '',
        'trainer_link': request.build_absolute_uri(reverse('trainer_edit', args=[trainer.id])) if trainer else '',
        'timestamp': timezone.now().isoformat(),
    }
    try:
        requests.post(TRACKING_URL, json=event)
    except requests.exceptions.RequestException:
        pass


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TrainerListView(ListView):
    model = Trainer
    template_name = 'trainers/trainer_list.html'

    def get(self, request, *args, **kwargs):
        send_event(request, 'view')
        return super().get(request, *args, **kwargs)


class TrainerCreateView(CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'trainers/trainer_form.html'
    success_url = reverse_lazy('trainer_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Trener został dodany pomyślnie.')
        send_event(self.request, 'add', self.object)
        return response


class TrainerUpdateView(UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'trainers/trainer_form.html'
    success_url = reverse_lazy('trainer_list')

    def form_valid(self, form):
        if form.has_changed():
            response = super().form_valid(form)
            messages.success(self.request, 'Trener został zaktualizowany pomyślnie.')
            send_event(self.request, 'edit', self.object)
            return response
        else:
            messages.info(self.request, 'Nie dokonano żadnych zmian.')
            return redirect(self.get_success_url())


class TrainerDeleteView(DeleteView):
    model = Trainer
    template_name = 'trainers/trainer_confirm_delete.html'
    success_url = reverse_lazy('trainer_list')

    def post(self, request, *args, **kwargs):
        trainer = self.get_object()
        messages.success(request, 'Trener został usunięty pomyślnie.')
        send_event(request, 'delete', trainer)
        return super().post(request, *args, **kwargs)


class LogListView(TemplateView):
    template_name = 'trainers/log_list.html'

    def translate_action(self, action_type):
        translations = {
            'view': 'Odwiedzenie strony',
            'add': 'Dodanie trenera',
            'edit': 'Edycja trenera',
            'delete': 'Usunięcie trenera'
        }
        return translations.get(action_type, action_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            response = requests.get('http://localhost:8001/tracking/logs/')
            logs = response.json()

            log_entries = []
            for log in logs:
                trainer_id = log.get('trainer_id')
                if trainer_id:
                    trainer_exists = Trainer.objects.filter(id=trainer_id).exists()
                    if trainer_exists:
                        link = format_html(
                            '<a href="{}">Trener ID {}</a>',
                            reverse('trainer_edit', args=[trainer_id]),
                            trainer_id
                        )
                    else:
                        link = f"Trener ID {trainer_id} został usunięty."
                else:
                    link = "-"

                raw_date = log.get("timestamp")
                formatted_date = parse(raw_date).strftime('%Y-%m-%d %H:%M:%S')

                log_entries.append({
                    "user_ip": log.get("ip"),
                    "action_type": self.translate_action(log.get("action_type")),
                    "trainer_link": link,
                    "action_date": formatted_date,
                })

            context['logs'] = log_entries
        except requests.exceptions.RequestException:
            context['logs'] = []

        return context
