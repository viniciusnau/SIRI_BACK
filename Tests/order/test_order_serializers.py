import pytest
from decimal import Decimal
import base64
from unittest.mock import patch
from user.serializers import ClientNameSerializer

from stock.serializers import (
    ProductMeSerializer,
    SupplierNameSerializer,
)

from order.serializers import (
    RetrieveOrderItemSerializer,
    OrderItemSerializer,
    RetrieveOrderSerializer,
    OrderSerializer,
    OrderMeSerializer,
    RetrieveStockWithdrawalSerializer,
    StockWithdrawalSerializer,
    RetrieveStockEntrySerializer,
    StockEntrySerializer,
    RetrieveSupplierOrderSerializer,
    SupplierOrderSerializer,
    RetrieveSupplierOrderItemSerializer,
    SupplierOrderItemSerializer,
    RetrieveProtocolWithdrawalSerializer,
    ProtocolWithdrawalSerializer,
    RetrieveMaterialsOrderSerializer,
    MaterialsOrderSerializer,
    client
)

@pytest.mark.django_db
def test_retrieve_order_item_serializer(order_item):
    serializer = RetrieveOrderItemSerializer(order_item)
    expected_data = {
        "id": order_item.id,
        "order": order_item.order.id,
        "product": ProductMeSerializer(order_item.product).data,
        "quantity": order_item.quantity,
        "added_quantity": order_item.added_quantity,
        "supplier_quantity": order_item.supplier_quantity,
        "supplier": SupplierNameSerializer(order_item.supplier).data,
        "created": order_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": order_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_order_item_serializer(order_item):
    serializer = OrderItemSerializer(order_item)
    expected_data = {
        "id": order_item.id,
        "order": order_item.order.id,
        "product": order_item.product.id,
        "quantity": order_item.quantity,
        "added_quantity": order_item.added_quantity,
        "supplier_quantity": order_item.supplier_quantity,
        "supplier": order_item.supplier.id,
        "created": order_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": order_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_retrieve_order_serializer(order, monkeypatch):
    serializer = RetrieveOrderSerializer(order)
    expected_file = "mocked_file_content"
    expected_encoded_file = base64.b64encode(expected_file.encode("utf-8")).decode("utf-8")

    def mock_get_object(Bucket, Key):
        class MockFileObject:
            def read(self):
                return b"mocked_file_content"

        return {"Body": MockFileObject()}

    monkeypatch.setattr(client, "get_object", mock_get_object)

    expected_data = {
        "id": order.id,
        "client": ClientNameSerializer(order.client).data,
        "file": expected_encoded_file,
        "is_sent": order.is_sent,
        "partially_added_to_stock": order.partially_added_to_stock,
        "completely_added_to_stock": order.completely_added_to_stock,
        "created": order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(order) == expected_encoded_file


@pytest.mark.django_db
def test_retrieve_order_serializer_with_none_file(order, monkeypatch):
    serializer = RetrieveOrderSerializer(order)
    def mock_get_object(Bucket, Key):
        class MockFileObject:
            def read(self):
                return b"mocked_file_content"

        return {"Body": MockFileObject()}

    monkeypatch.setattr(client, "get_object", mock_get_object)
    order.file = None
    order.save()
    expected_data = {
        "id": order.id,
        "client": ClientNameSerializer(order.client).data,
        "file": None,
        "is_sent": order.is_sent,
        "partially_added_to_stock": order.partially_added_to_stock,
        "completely_added_to_stock": order.completely_added_to_stock,
        "created": order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(order) is None


@pytest.mark.django_db
def test_order_serializer(order, monkeypatch):
    serializer = OrderSerializer(order)

    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{order.id}"

    def generate_presigned_url_mock(*args, **kwargs):
        url = f"https://local-sed.s3.amazonaws.com/protocols/{order.id}"
        return url

    monkeypatch.setattr(client, "generate_presigned_url", generate_presigned_url_mock)
    expected_data = {
        "id": order.id,
        "client": order.client.id,
        "is_sent": order.is_sent,
        "partially_added_to_stock": order.partially_added_to_stock,
        "completely_added_to_stock": order.completely_added_to_stock,
        "file": expected_url,
        "created": order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(order) == expected_url

@pytest.mark.skip
def test_order_me_serializer(order):
    pass

@pytest.mark.skip
def test_retrieve_stock_with_drawal_serializer(stock_with_drawal):
    pass
@pytest.mark.skip
def test_stock_with_drawal_serializer(stock_with_drawal):
    pass
@pytest.mark.skip
def test_retrieve_stock_entry_serializer(stock_entry):
    pass

@pytest.mark.skip
def test_stock_entry_serializer(stock_entry):
    pass

@pytest.mark.skip
def test_retrieve_supplier_order_serializer(supplier_oder):
    pass

@pytest.mark.skip
def test_supplier_order_serializer(supplier_oder):
    pass

@pytest.mark.skip
def test_retrieve_supplier_order_item_serializer(supplier_order_item):
    pass

@pytest.mark.skip
def test_supplier_order_item_serializer(supplier_order_item):
    pass

@pytest.mark.skip
def test_retrieve_protocol_with_drawal_serializer(protocol_with_drawal):
    pass

@pytest.mark.skip
def test_protocol_with_drawal_serializer(protocol_with_drawal):
    pass

@pytest.mark.django_db
def test_retrieve_materials_order_serializer(materials_order, monkeypatch):
    serializer = RetrieveMaterialsOrderSerializer(materials_order)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{materials_order.id}"

    def generate_presigned_url_mock(*args, **kwargs):
        code = materials_order.id
        url = f"https://local-sed.s3.amazonaws.com/protocols/{code}"
        return url

    monkeypatch.setattr(client, "generate_presigned_url", generate_presigned_url_mock)
    expected_data = {
        "id": materials_order.id,
        "supplier": SupplierNameSerializer(materials_order.supplier).data,
        "file": expected_url,
        "date_range": materials_order.date_range,
        "created": materials_order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": materials_order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(materials_order) == expected_url
@pytest.mark.django_db
def test_retrieve_materials_order_serializer_with_none_file(materials_order, monkeypatch):
    serializer = RetrieveMaterialsOrderSerializer(materials_order)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{materials_order.id}"

    def generate_presigned_url_mock(*args, **kwargs):
        code = materials_order.id
        url = f"https://local-sed.s3.amazonaws.com/protocols/{code}"
        return url

    monkeypatch.setattr(client, "generate_presigned_url", generate_presigned_url_mock)
    materials_order.file = False
    materials_order.save()
    expected_data = {
        "id": materials_order.id,
        "supplier": SupplierNameSerializer(materials_order.supplier).data,
        "file": None,
        "date_range": materials_order.date_range,
        "created": materials_order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": materials_order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(materials_order) is None
@pytest.mark.django_db
def test_materials_order_serializer(materials_order, monkeypatch):
    serializer = MaterialsOrderSerializer(materials_order)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{materials_order.id}"

    def generate_presigned_url_mock(*args, **kwargs):
        code = materials_order.id
        url = f"https://local-sed.s3.amazonaws.com/protocols/{code}"
        return url

    monkeypatch.setattr(client, "generate_presigned_url", generate_presigned_url_mock)
    expected_data = {
        "id": materials_order.id,
        "supplier": materials_order.supplier.id,
        "file": expected_url,
        "date_range": materials_order.date_range,
        "created": materials_order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": materials_order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(materials_order) == expected_url

@pytest.mark.django_db
def test_materials_order_serializer_with_none_file(materials_order, monkeypatch):
    serializer = MaterialsOrderSerializer(materials_order)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{materials_order.id}"

    def generate_presigned_url_mock(*args, **kwargs):
        code = materials_order.id
        url = f"https://local-sed.s3.amazonaws.com/protocols/{code}"
        return url

    monkeypatch.setattr(client, "generate_presigned_url", generate_presigned_url_mock)
    materials_order.file = False
    materials_order.save()
    expected_data = {
        "id": materials_order.id,
        "supplier": materials_order.supplier.id,
        "file": None,
        "date_range": materials_order.date_range,
        "created": materials_order.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": materials_order.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(materials_order) is None
