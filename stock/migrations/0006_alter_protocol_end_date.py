# Generated by Django 4.1.7 on 2023-06-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0005_protocol_end_date_protocol_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocol",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
