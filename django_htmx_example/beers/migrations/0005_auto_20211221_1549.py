# Generated by Django 3.1.13 on 2021-12-21 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beers', '0004_auto_20211217_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='beer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
