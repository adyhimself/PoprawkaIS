from django import forms
from django.utils.translation import gettext_lazy as _
from intl_tel_input.widgets import IntlTelInputWidget
from phonenumber_field.formfields import PhoneNumberField
from .models import Trainer


class TrainerForm(forms.ModelForm):
    phone = PhoneNumberField(
        widget=IntlTelInputWidget(
            attrs={
                'class': 'form-control intl-tel-input',
                'data-default-code': 'pl',
                'data-allow-dropdown': 'true',
                'data-preferred-countries': 'pl',
            }
        ),
        label=_('Telefon'),
        error_messages={
            'invalid': _('Wprowadź poprawny numer telefonu'),
            'required': _('To pole jest wymagane.'),
        }
    )

    class Meta:
        model = Trainer
        fields = ['first_name', 'last_name', 'email', 'phone']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        allowed_chars = ["-", "'", " "]
        if not all(char.isalpha() or char in allowed_chars for char in first_name):
            raise forms.ValidationError(_('Wpisz poprawne imię.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        allowed_chars = ["-", "'", " "]
        if not all(char.isalpha() or char in allowed_chars for char in last_name):
            raise forms.ValidationError(_('Wpisz poprawne nazwisko.'))
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        trainer_id = self.instance.pk
        if Trainer.objects.filter(email=email).exclude(pk=trainer_id).exists():
            raise forms.ValidationError(_('Trener z tym adresem email już istnieje.'))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        trainer_id = self.instance.pk
        if Trainer.objects.filter(phone=phone).exclude(pk=trainer_id).exists():
            raise forms.ValidationError(_('Trener z tym numerem telefonu już istnieje.'))
        return phone
