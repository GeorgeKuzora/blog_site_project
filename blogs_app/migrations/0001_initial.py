# Generated by Django 4.1 on 2022-09-26 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogpostModel",
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
                ("title", models.CharField(max_length=150, verbose_name="Заголовок")),
                ("contents", models.TextField(verbose_name="Содержание")),
                (
                    "date_created",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                ("image", models.ImageField(upload_to="files/")),
                (
                    "author",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Автор",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]