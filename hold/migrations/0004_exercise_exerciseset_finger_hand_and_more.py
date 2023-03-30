# Generated by Django 4.1.7 on 2023-03-30 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_measurement.models
import measurement.measures.mass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hold', '0003_climbingequipment_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('uses_bodyweight', models.BooleanField(default=False, verbose_name='uses bodyweight')),
            ],
            options={
                'verbose_name': 'Exercise',
                'verbose_name_plural': 'Exercise',
            },
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hold_duration', models.FloatField()),
                ('weight', django_measurement.models.MeasurementField(measurement=measurement.measures.mass.Mass)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Finger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('thumb', 'Thumb'), ('index', 'Index'), ('middle', 'Middle'), ('ring', 'Ring'), ('pinky', 'Pinky')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Left', 'Left'), ('Right', 'Right'), ('Both', 'Both')], max_length=10)),
                ('fingers', models.ManyToManyField(to='hold.finger')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSetHandConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.exerciseset')),
                ('fingers', models.ManyToManyField(to='hold.finger')),
                ('hand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.hand')),
            ],
            options={
                'verbose_name_plural': 'Exercise Set Hand Configurations',
            },
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='fingers',
            field=models.ManyToManyField(blank=True, to='hold.finger'),
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='hands',
            field=models.ManyToManyField(blank=True, to='hold.hand'),
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ExerciseHandConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.exercise')),
                ('fingers', models.ManyToManyField(to='hold.finger')),
                ('hand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.hand')),
            ],
        ),
    ]