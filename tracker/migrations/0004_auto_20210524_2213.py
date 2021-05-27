# Generated by Django 3.1.7 on 2021-05-24 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20210413_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'active'), (2, 'paused'), (3, 'finished')], db_index=True, default=1, verbose_name='Task status'),
        ),
    ]
