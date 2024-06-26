# Generated by Django 5.0.6 on 2024-06-19 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barberapp', '0002_remove_booking_customer_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='barberapp.service'),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='barberapp.staff'),
        ),
    ]
