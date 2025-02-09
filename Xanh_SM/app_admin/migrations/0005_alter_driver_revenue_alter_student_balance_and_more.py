# Generated by Django 5.1.4 on 2025-02-06 08:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0004_trip_distance_alter_driver_revenue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='revenue',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='balance',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='trip',
            name='distance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
