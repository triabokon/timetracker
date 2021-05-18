# Generated by Django 3.1.7 on 2021-04-13 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tasks',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
