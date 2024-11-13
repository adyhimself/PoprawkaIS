from django.db import models
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError

ALLOWED_ACTIONS = {'view', 'edit', 'add', 'delete'}
MAX_LINK_LENGTH = 2000


class Event(models.Model):
    objects = None
    ip = models.CharField(max_length=50)
    action_type = models.CharField(max_length=100)
    trainer_id = models.IntegerField(null=True, blank=True)
    trainer_link = models.URLField(blank=True)
    timestamp = models.DateTimeField()

    def clean(self):
        if self.action_type not in ALLOWED_ACTIONS:
            raise ValidationError({'action_type': 'Nieprawidłowy typ akcji.'})

        if len(self.trainer_link) > MAX_LINK_LENGTH:
            raise ValidationError({'trainer_link': f'Link nie może przekraczać {MAX_LINK_LENGTH} znaków.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action_type} at {localtime(self.timestamp).strftime('%Y-%m-%d %H:%M:%S%z')[:22]}:{localtime(self.timestamp).strftime('%Y-%m-%d %H:%M:%S%z')[22:]}"
