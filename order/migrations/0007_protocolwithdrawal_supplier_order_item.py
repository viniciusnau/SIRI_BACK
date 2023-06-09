# Generated by Django 4.1.7 on 2023-07-03 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0006_order_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="protocolwithdrawal",
            name="supplier_order_item",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="order.supplierorderitem",
            ),
        ),
    ]
