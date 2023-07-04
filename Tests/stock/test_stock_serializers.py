import pytest
from django.test import TestCase
from django.utils import timezone
from stock.serializers import (
    AccountantReportCategorySerializer,
    AccountantReportSerializer,
    BiddingExemptionSerializer,
    CategorySerializer,
    DispatchReportSerializer,
    EmailSerializer,
    InvoiceCodeSerializer,
    InvoiceSerializer,
    MeasureNameSerializer,
    MeasureSerializer,
    ProductMeSerializer,
    ProductSerializer,
    ProtocolCodeSerializer,
    ProtocolItemSerializer,
    ProtocolSerializer,
    PublicDefenseSerializer,
    ReceivingReportSerializer,
    RetrieveBiddingExemptionSerializer,
    RetrieveDispatchReportSerializer,
    RetrieveInvoiceSerializer,
    RetrieveProductSerializer,
    RetrieveProtocolItemSerializer,
    RetrieveProtocolSerializer,
    RetrieveReceivingReportSerializer,
    RetrieveSectorSerializer,
    RetrieveStockItemSerializer,
    RetrieveStockSerializer,
    RetrieveSupplierSerializer,
    SectorSerializer,
    StockItemMeSerializer,
    StockItemSerializer,
    StockSerializer,
    SupplierNameSerializer,
    SupplierSerializer,
)


@pytest.mark.django_db
def test_public_defense_serializer(public_defense):
    serializer = PublicDefenseSerializer(public_defense)
    expected_data = {
        "id": public_defense.id,
        "name": public_defense.name,
        "district": public_defense.district,
        "address": public_defense.address,
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_retrieve_stock_serializer(stock):
    serializer = RetrieveStockSerializer(stock)
    expected_data = {
        "sector": str(stock.sector),
        "id": stock.id,
        "created": stock.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": stock.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_stock_serializer(stock):
    serializer = StockSerializer(stock)
    expected_data = {
        "sector": stock.sector.id,
        "id": stock.id,
        "created": stock.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": stock.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_sector_serializer(sector):
    serializer = RetrieveSectorSerializer(sector)
    expected_data = {
        "name": None,
        "public_defense": None,
        "created": None,
        "updated": None,
    }
    assert serializer.data == expected_data