# Generated by Django 4.1.7 on 2023-05-30 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="accountantreport",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="biddingexemption",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ("-created",),
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
        migrations.AlterModelOptions(
            name="categorybalance",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="dispatchreport",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="invoice",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="measure",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="protocol",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="protocolitem",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="publicdefense",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="receivingreport",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="sector",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="stock",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="stockitem",
            options={"ordering": ("-created",)},
        ),
        migrations.AlterModelOptions(
            name="supplier",
            options={"ordering": ("-created",)},
        ),
        migrations.AddField(
            model_name="accountantreport",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="accountantreport",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="biddingexemption",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="biddingexemption",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="category",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="category",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="categorybalance",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="categorybalance",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="measure",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="measure",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="protocol",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="protocol",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="protocolitem",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="protocolitem",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="publicdefense",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="publicdefense",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="sector",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="sector",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="stock",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="stock",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="supplier",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="supplier",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="dispatchreport",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="dispatchreport",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="product",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="receivingreport",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="receivingreport",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]