import base64
import os

import boto3
from rest_framework import serializers

from stock.serializers import (
    ProductMeSerializer,
    ProtocolCodeSerializer,
    PublicDefenseSerializer,
    RetrieveProtocolItemSerializer,
    StockItemMeSerializer,
    SupplierNameSerializer,
)
from user.serializers import ClientNameSerializer

from .models import (
    MaterialsOrder,
    Order,
    OrderItem,
    ProtocolWithdrawal,
    StockEntry,
    StockWithdrawal,
    SupplierOrder,
    SupplierOrderItem,
)

client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION_NAME"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


class RetrieveOrderItemSerializer(serializers.ModelSerializer):
    product = ProductMeSerializer()
    supplier = SupplierNameSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class RetrieveOrderSerializer(serializers.ModelSerializer):
    client = ClientNameSerializer()
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            bucket_name = os.environ.get("AWS_BUCKET_NAME")
            key = f"confirm-order/{obj.id}"
            file_obj = client.get_object(Bucket=bucket_name, Key=key)
            file_content = file_obj['Body'].read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
            return encoded_file
        return None

    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                "Key": f"confirm-order/{obj.id}",
            },
            ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
            HttpMethod="GET",
        )
        return url

    class Meta:
        model = Order
        fields = "__all__"


class OrderMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "is_sent",
            "partially_added_to_stock",
            "completely_added_to_stock",
            "created",
            "updated",
        )


class RetrieveStockWithdrawalSerializer(serializers.ModelSerializer):
    stock_item = StockItemMeSerializer()

    class Meta:
        model = StockWithdrawal
        fields = "__all__"


class StockWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockWithdrawal
        fields = "__all__"


class RetrieveStockEntrySerializer(serializers.ModelSerializer):
    stock_item = StockItemMeSerializer()
    order_item = OrderItemSerializer()

    class Meta:
        model = StockEntry
        fields = "__all__"


class StockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockEntry
        fields = "__all__"


class RetrieveSupplierOrderSerializer(serializers.ModelSerializer):
    client = ClientNameSerializer()
    supplier = SupplierNameSerializer()
    protocol = ProtocolCodeSerializer()
    public_defense = PublicDefenseSerializer()

    class Meta:
        model = SupplierOrder
        fields = "__all__"


class SupplierOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOrder
        fields = "__all__"


class RetrieveSupplierOrderItemSerializer(serializers.ModelSerializer):
    product = ProductMeSerializer()

    class Meta:
        model = SupplierOrderItem
        fields = "__all__"


class SupplierOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOrderItem
        fields = "__all__"


class RetrieveProtocolWithdrawalSerializer(serializers.ModelSerializer):
    protocol_item = RetrieveProtocolItemSerializer()

    class Meta:
        model = ProtocolWithdrawal
        fields = "__all__"


class ProtocolWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolWithdrawal
        fields = "__all__"


class RetrieveMaterialsOrderSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    supplier = SupplierNameSerializer()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"materials-order/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = MaterialsOrder
        fields = ["id", "supplier", "file", "date_range", "created", "updated"]


class MaterialsOrderSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            code = obj.id
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.environ.get("AWS_BUCKET_NAME"),
                    "Key": f"materials-order/{code}",
                },
                ExpiresIn=os.environ.get("AWS_EXPIRES_SECONDS"),
                HttpMethod="GET",
            )
            return url
        return None

    class Meta:
        model = MaterialsOrder
        fields = ["id", "supplier", "file", "date_range", "created", "updated"]
