# Generated by Django 4.1 on 2022-10-31 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blogs_app", "0005_uploadcsvfile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpostmodel",
            options={"verbose_name": "blog", "verbose_name_plural": "blogs"},
        ),
        migrations.AlterModelOptions(
            name="uploadcsvfile",
            options={"verbose_name": "csv file", "verbose_name_plural": "csv files"},
        ),
        migrations.AlterModelOptions(
            name="uploadimagemodel",
            options={"verbose_name": "image", "verbose_name_plural": "images"},
        ),
        migrations.AlterField(
            model_name="blogpostmodel",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Author",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="blogpostmodel",
            name="contents",
            field=models.TextField(verbose_name="Contents"),
        ),
        migrations.AlterField(
            model_name="blogpostmodel",
            name="date_created",
            field=models.DateField(auto_now_add=True, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="blogpostmodel",
            name="title",
            field=models.CharField(max_length=150, verbose_name="Title"),
        ),
    ]
