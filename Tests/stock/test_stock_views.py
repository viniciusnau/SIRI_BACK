import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
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
    client
)

from stock.views import (
    client,
    AllStocksView,
    StockListCreateView,
    StockRetrieveUpdateDestroyView,
    AllSectorsView,
    SectorListCreateView,
    SectorRetrieveUpdateDestroyView,
    AllPublicDefensesView,
    PublicDefenseListCreateView,
    PublicDefenseRetrieveUpdateDestroyView,
    AllCategoriesView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    AllMeasuresView,
    MeasureListCreateView,
    MeasureRetrieveUpdateDestroyView,
    AllProductsView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    StockItemListCreateView,
    StockItemRetrieveUpdateDestroyView,
    SupplierListCreateView,
    AllSuppliersView,
    SupplierRetrieveUpdateDestroyView,
    AllProtocolsView,
    ProtocolListCreateView,
    ProtocolRetrieveUpdateDestroyView,
    ProtocolItemListView,
    ProtocolItemListCreateView,
    ProtocolItemRetrieveUpdateDestroyView,
    AllInvoicesView,
    InvoiceListCreateView,
    InvoiceRetrieveUpdateDestroyView,
    ReceivingReportListCreateView,
    ReceivingReportRetrieveUpdateDestroyView,
    DispatchReportListCreateView,
    DispatchReportRetrieveUpdateDestroyView,
    BiddingExemptionListCreateView,
    BiddingExemptionRetrieveUpdateDestroyView,
    AccountantReportListCreateView,
    AccountantReportRetrieveUpdateDestroyView,
    StockReport,
    WarehouseItems,
    EmailView,
)

@pytest.mark.django_db
def test_all_stocks_view(patch_stock_objects_all, rf, super_user, stock, stock_extra):
    factory = rf
    url = reverse("stock:all-stocks")
    expected_data = RetrieveStockSerializer([stock_extra, stock], many=True).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = AllStocksView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data


@pytest.mark.django_db
def test_stock_list_create_view(patch_stock_objects_all, patch_stock_objects_order_by_id, rf, super_user, stock, stock_extra):
    factory = rf
    url = reverse("stock:stock-list-create")
    expected_data = RetrieveStockSerializer([stock, stock_extra], many=True).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = StockListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("results") == expected_data


@pytest.mark.django_db
def test_stock_list_create_view_post(patch_stock_objects_all, patch_stock_objects_order_by_id, rf, super_user, stock, stock_extra):
    factory = rf
    url = reverse("stock:stock-list-create")
    expected_data = StockSerializer(stock).data

    request = factory.post(url, {})
    force_authenticate(request, user=super_user)
    response = StockListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get == expected_data


@pytest.mark.skip
def test_stock_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_sectors_views():
    pass

@pytest.mark.skip
def test_sector_list_create_view():
    pass

@pytest.mark.skip
def test_sector_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_public_defenses_view():
    pass

@pytest.mark.skip
def test_public_defense_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_categories_view():
    pass

@pytest.mark.skip
def test_category_list_create_view():
    pass

@pytest.mark.skip
def test_category_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_measure_view():
    pass

@pytest.mark.skip
def test_measure_list_create_view():
    pass

@pytest.mark.skip
def test_measure_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_products_view():
    pass

@pytest.mark.skip
def test_product_list_create_view():
    pass

@pytest.mark.skip
def test_product_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_stock_item_list_create_view():
    pass

@pytest.mark.skip
def test_stock_item_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_supplier_list_create_view():
    pass

@pytest.mark.skip
def test_all_suppliers_view():
    pass

@pytest.mark.skip
def test_supplier_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_protocols_view():
    pass

@pytest.mark.skip
def test_protocol_list_create_view():
    pass

@pytest.mark.skip
def test_protocol_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_protocol_item_list_view():
    pass

@pytest.mark.skip
def test_protocol_item_list_create_view():
    pass

@pytest.mark.skip
def test_protocol_item_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_all_invoices_view():
    pass

@pytest.mark.skip
def test_invoice_list_create_view():
    pass

@pytest.mark.skip
def test_invoice_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_receiving_report_list_create_view():
    pass

@pytest.mark.skip
def test_receiving_report_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_dispatch_report_list_create_view():
    pass

@pytest.mark.skip
def test_dispatch_report_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_bidding_exemption_list_create_view():
    pass

@pytest.mark.skip
def test_bidding_exemption_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_accountant_report_list_create_view():
    pass

@pytest.mark.skip
def test_accountant_report_retrieve_update_destroy_view():
    pass

@pytest.mark.skip
def test_stock_report():
    pass

@pytest.mark.skip
def test_warehouse_items():
    pass

@pytest.mark.skip
def test_email_view():
    pass