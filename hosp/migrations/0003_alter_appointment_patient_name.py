# Generated by Django 4.2.2 on 2023-07-31 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp', '0002_alter_appointment_patient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient_name',
            field=models.CharField(max_length=255),
        ),
    ]