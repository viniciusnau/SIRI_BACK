# Generated by Django 4.1.7 on 2023-06-16 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0008_alter_protocol_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="dispatchreport",
            name="stock_item",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.stockitem",
            ),
        ),
        migrations.AddField(
            model_name="receivingreport",
            name="stock_item",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.stockitem",
            ),
        ),
    ]
