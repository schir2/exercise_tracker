# Generated by Django 4.1.7 on 2023-04-02 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hold', '0014_remove_exercise_climbing_hold_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseset',
            name='climbing_hold',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hold.climbinghold'),
            preserve_default=False,
        ),
    ]