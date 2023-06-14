import os

import boto3
from rest_framework import serializers

from .models import (
    AccountantReport,
    BiddingExemption,
    Category,
    DispatchReport,
    Invoice,
    Measure,
    Product,
    Protocol,
    ProtocolItem,
    PublicDefense,
    ReceivingReport,
    Sector,
    Stock,
    StockItem,
    Supplier,
)

client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION_NAME"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


class RetrieveStockSerializer(serializers.ModelSerializer):
    sector = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class PublicDefenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicDefense
        fields = ["id", "name", "district", "address"]


class RetrieveSectorSerializer(serializers.ModelSerializer):
    public_defense = PublicDefenseSerializer()

    class Meta:
        model = Sector
        fields = "__all__"


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "code"]


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = "__all__"


class RetrieveProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    measure = MeasureSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class MeasureNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ("name",)


class ProductMeSerializer(serializers.ModelSerializer):
    measure = MeasureNameSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "measure",
            "description",
        )


class RetrieveStockItemSerializer(serializers.ModelSerializer):
    stock = RetrieveStockSerializer()
    product = ProductMeSerializer()

    class Meta:
        model = StockItem
        fields = "__all__"

    def get_stock(self, obj):
        return RetrieveStockSerializer(obj.stock).data


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = "__all__"


class StockItemMeSerializer(serializers.ModelSerializer):
    product = ProductMeSerializer()

    class Meta:
        model = StockItem
        fields = ("id", "product", "quantity", "created", "updated")

    def get_stock(self, obj):
        return RetrieveStockSerializer(obj.stock).data


class RetrieveSupplierSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name"]


class RetrieveProtocolSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    supplier = SupplierNameSerializer()
    category = CategorySerializer()

    def get_file(self, obj):
        code = obj.code
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"protocols/{code}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = Protocol
        fields = ["id", "code", "supplier", "category", "file"]


class ProtocolSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        code = obj.code
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"protocols/{code}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = Protocol
        fields = ["id", "code", "supplier", "category", "file"]


class ProtocolCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = ["id", "code"]


class RetrieveProtocolItemSerializer(serializers.ModelSerializer):
    product = ProductMeSerializer()

    class Meta:
        model = ProtocolItem
        fields = "__all__"


class ProtocolItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolItem
        fields = "__all__"


class RetrieveInvoiceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    supplier = SupplierNameSerializer()
    public_defense = PublicDefenseSerializer()

    def get_file(self, obj):
        code = obj.code
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"invoices/{code}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = Invoice
        fields = [
            "id",
            "total_value",
            "public_defense",
            "supplier",
            "file",
            "code",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class InvoiceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        code = obj.code
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"invoices/{code}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = Invoice
        fields = [
            "id",
            "total_value",
            "public_defense",
            "supplier",
            "file",
            "code",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class RetrieveReceivingReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    product = ProductMeSerializer()
    supplier = SupplierNameSerializer()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"receiving-reports/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = ReceivingReport
        fields = [
            "id",
            "product",
            "quantity",
            "supplier",
            "file",
            "description",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class ReceivingReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"receiving-reports/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = ReceivingReport
        fields = [
            "id",
            "product",
            "quantity",
            "supplier",
            "file",
            "description",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class RetrieveDispatchReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    product = ProductMeSerializer()
    public_defense = PublicDefenseSerializer()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"dispatch-reports/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = DispatchReport
        fields = [
            "id",
            "product",
            "quantity",
            "public_defense",
            "file",
            "description",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class DispatchReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"dispatch-reports/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = DispatchReport
        fields = [
            "id",
            "product",
            "quantity",
            "public_defense",
            "file",
            "description",
            "created",
            "updated",
        ]
        read_only_fields = ["created", "updated"]


class InvoiceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "code"]


class RetrieveBiddingExemptionSerializer(serializers.ModelSerializer):
    product = ProductMeSerializer()
    invoice = InvoiceCodeSerializer()

    class Meta:
        model = BiddingExemption
        fields = "__all__"


class BiddingExemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingExemption
        fields = "__all__"


class AccountantReportSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        month = obj.month
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"accountant-reports/{month}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = AccountantReport
        fields = [
            "id",
            "month",
            "total_previous_value",
            "total_entry_value",
            "file",
            "total_output_value",
            "total_current_value",
        ]


class AccountantReportCategorySerializer(serializers.Serializer):
    code = serializers.CharField(source="product__category__code")
    name = serializers.CharField(source="product__category__name")
    entry_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    output_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)
    previous_balance = serializers.DecimalField(max_digits=18, decimal_places=2)
    current_balance = serializers.DecimalField(max_digits=18, decimal_places=2)


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    message = serializers.CharField()
