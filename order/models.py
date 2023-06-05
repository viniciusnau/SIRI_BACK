from django.db import models
from django.utils import timezone

from stock.models import (
    Category,
    Product,
    Protocol,
    ProtocolItem,
    PublicDefense,
    StockItem,
    Supplier,
)
from user.models import Client


class Order(models.Model):
    client = models.ForeignKey(
        Client, related_name="client", on_delete=models.DO_NOTHING
    )
    is_sent = models.BooleanField(default=False)
    partially_added_to_stock = models.BooleanField(default=False)
    completely_added_to_stock = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    added_quantity = models.PositiveIntegerField(default=0)
    supplier_quantity = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return (
            "order: "
            + str(self.order.id)
            + " - "
            + self.order.client.name
            + " - "
            + self.order.client.stock.sector.name
            + " - "
            + self.order.client.stock.sector.public_defense.name
            + " - "
            + str(self.product)
        )


class StockWithdrawal(models.Model):
    stock_item = models.ForeignKey(
        StockItem, related_name="stock_withdraw", on_delete=models.CASCADE
    )
    withdraw_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    withdraw_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"StockWithdrawal {self.id}"


class StockEntry(models.Model):
    stock_item = models.ForeignKey(
        StockItem, related_name="stock_entry", on_delete=models.CASCADE
    )
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    entry_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    entry_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)
        constraints = [
            models.UniqueConstraint(
                fields=["order_item"], name="%(app_label)s_%(class)s_unique"
            )
        ]

    def __str__(self):
        return f"StockEntry {self.id}"


class SupplierOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    public_defense = models.ForeignKey(PublicDefense, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"SupplierOrder {self.id}"


class SupplierOrderItem(models.Model):
    supplier_order = models.ForeignKey(SupplierOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="supplier_order_item", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"SupplierOrderItem {self.id}"


class ProtocolWithdrawal(models.Model):
    protocol_item = models.ForeignKey(
        ProtocolItem, related_name="protocol_withdraw", on_delete=models.CASCADE
    )
    withdraw_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    withdraw_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"ProtocolWithdrawal {self.id}"


class MaterialsOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.TextField(blank=True, default=None, null=True)
    date_range = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"MaterialsOrder {self.id}"
