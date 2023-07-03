import pytest
from django.test import TestCase
from django.utils import timezone
from .serializers import (
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
        "created": stock.created,
        "updated": stock.updated,
    }

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_stock_serializer(stock):
    serializer = StockSerializer(stock)
    expected_data = {
        "nome": "juninho"
    }