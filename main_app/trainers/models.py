from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Trainer(models.Model):
    objects = None
    first_name = models.CharField(max_length=100, verbose_name='Imię')
    last_name = models.CharField(max_length=100, verbose_name='Nazwisko')
    email = models.EmailField(_('Email'), unique=True)
    phone = PhoneNumberField(_('Telefon'), region=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
