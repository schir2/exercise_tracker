# Generated by Django 4.1.7 on 2023-03-31 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hold', '0008_remove_exercisesethandconfiguration_exercise_set_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseset',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date'),
            preserve_default=False,
        ),
    ]
