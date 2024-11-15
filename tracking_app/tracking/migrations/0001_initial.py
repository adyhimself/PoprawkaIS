# Generated by Django 5.1.1 on 2024-09-28 00:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.CharField(max_length=50)),
                ("action_type", models.CharField(max_length=100)),
                ("trainer_id", models.IntegerField(blank=True, null=True)),
                ("trainer_link", models.URLField(blank=True)),
                ("timestamp", models.DateTimeField()),
            ],
        ),
    ]
