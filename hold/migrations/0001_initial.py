# Generated by Django 4.1.7 on 2023-03-30 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClimbingEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('equipment_type', models.CharField(choices=[('HB', 'Hangboard'), ('PB', 'Pinch Block'), ('CB', 'Campus Board'), ('TB', 'Training Board')], max_length=2, verbose_name='equipment type')),
                ('manufacturer', models.CharField(blank=True, max_length=100, null=True, verbose_name='manufacturer')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'climbing equipment',
                'verbose_name_plural': 'climbing equipment',
            },
        ),
        migrations.CreateModel(
            name='ClimbingHold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('hold_type', models.CharField(choices=[('JG', 'Jug'), ('SL', 'Sloper'), ('CR', 'Crimp'), ('PC', 'Pinch'), ('PK', 'Pocket'), ('SP', 'Sidepull'), ('GT', 'Gaston'), ('UC', 'Undercling')], max_length=2, verbose_name='hold type')),
                ('size', models.FloatField(help_text='Size of the edge, pocket, or other dimensions as applicable', verbose_name='size')),
                ('depth', models.FloatField(help_text='Depth of the hold, if applicable', verbose_name='depth')),
                ('angle', models.FloatField(blank=True, help_text='Angle of the hold, if applicable', null=True, verbose_name='angle')),
                ('climbing_equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hold.climbingequipment', verbose_name='climbing equipment')),
            ],
            options={
                'verbose_name': 'climbing hold',
                'verbose_name_plural': 'climbing holds',
            },
        ),
    ]