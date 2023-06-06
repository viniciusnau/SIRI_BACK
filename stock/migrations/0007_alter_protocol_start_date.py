# Generated by Django 4.1.7 on 2023-06-06 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0006_alter_protocol_end_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocol",
            name="start_date",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
