# Generated by Django 5.1.1 on 2024-09-29 21:23

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trainers", "0002_alter_trainer_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trainer",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="trainer",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None, verbose_name="Telefon"
            ),
        ),
    ]
