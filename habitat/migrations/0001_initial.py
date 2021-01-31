# Generated by Django 3.1.5 on 2021-01-31 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unique_bid_number", models.CharField(max_length=255)),
                ("accepted_or_rejected", models.CharField(max_length=255)),
                ("delivery_date", models.DateField()),
            ],
        ),
    ]
