# Generated by Django 5.0.7 on 2024-08-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("due_date", models.DateField()),
                ("completed", models.BooleanField(default=False)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
            options={
                "ordering": ["due_date"],
            },
        ),
    ]