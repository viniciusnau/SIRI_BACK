# Generated by Django 4.1.7 on 2023-06-16 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0009_dispatchreport_stock_item_receivingreport_stock_item"),
        ("order", "0004_alter_materialsorder_created_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockentry",
            name="invoice",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="stock.invoice",
            ),
        ),
    ]