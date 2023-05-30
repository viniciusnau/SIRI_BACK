from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class PublicDefense(models.Model):
    name = models.CharField("Name", max_length=255)
    district = models.CharField("District", max_length=255)
    address = models.CharField("Address", max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Sector(models.Model):
    name = models.CharField("Name", max_length=255)
    public_defense = models.ForeignKey(
        PublicDefense, on_delete=models.DO_NOTHING, related_name="sectors"
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Stock(models.Model):
    sector = models.ForeignKey(
        Sector,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        related_name="stocks",
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sector.name + " - " + self.sector.public_defense.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sector",
                ],
                name="%(app_label)s_%(class)s_unique",
            )
        ]
        ordering = ("-created",)


class Category(models.Model):
    name = models.CharField("Name", max_length=200)
    sector = models.ManyToManyField(Sector, related_name="Category")
    code = models.CharField("Code", max_length=200)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Measure(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    measure = models.ForeignKey(Measure, on_delete=models.DO_NOTHING)
    price = models.FloatField(
        validators=[
            MinValueValidator(0),
        ],
        default=0.00,
    )
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    code = models.CharField("Name", max_length=255)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class StockItem(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock", blank=False, null=False
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (
            self.stock.sector.name
            + " - "
            + self.stock.sector.public_defense.name
            + " - "
            + self.product.name
        )

    class Meta:
        ordering = ("-created",)


class Supplier(models.Model):
    name = models.CharField("Name", max_length=255)
    agent = models.CharField("Agent", max_length=255)
    category = models.ManyToManyField(Category)
    address = models.CharField("Address", max_length=255)
    email = models.EmailField(max_length=254)
    phone = models.CharField("Phone", max_length=14)
    ein = models.CharField("Employer Identification Number", max_length=25)
    ssn = models.CharField("Social Security Number", max_length=25)
    nic = models.CharField("National Identity Card", max_length=25)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-created",)


class Protocol(models.Model):
    code = models.CharField("Code", null=True, max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ("-created",)


class ProtocolItem(models.Model):
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="protocol",
        blank=False,
        null=False,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    original_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (
            self.protocol.code
            + " - "
            + self.protocol.supplier.name
            + " - "
            + self.product.name
        )

    class Meta:
        ordering = ("-created",)


class Invoice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    public_defense = models.ForeignKey(
        PublicDefense, null=True, on_delete=models.CASCADE
    )
    code = models.CharField("Code", null=True, max_length=255)
    total_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ("-created",)


class ReceivingReport(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    file = models.TextField(blank=True, default=None, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ReceivingReport {self.id}"

    class Meta:
        ordering = ("-created",)


class DispatchReport(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    public_defense = models.ForeignKey(PublicDefense, on_delete=models.CASCADE)
    file = models.TextField(blank=True, default=None, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"DispatchReport {self.id}"

    class Meta:
        ordering = ("-created",)


class BiddingExemption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"BiddingExemption {self.id}"

    class Meta:
        ordering = ("-created",)


class AccountantReport(models.Model):
    month = models.TextField(blank=False, null=False)
    total_previous_value = models.PositiveIntegerField(default=0)
    total_entry_value = models.PositiveIntegerField(default=0)
    total_output_value = models.PositiveIntegerField(default=0)
    total_current_value = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"AccountantReport {self.id}"

    class Meta:
        ordering = ("-created",)


class CategoryBalance(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="balances"
    )
    date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"CategoryBalance {self.id}"

    class Meta:
        ordering = ("-created",)
