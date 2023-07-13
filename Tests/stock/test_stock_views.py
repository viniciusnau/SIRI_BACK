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
def test_stock_list_create_view_get(rf, super_user, stock, stock_extra):
    factory = rf
    url = reverse("stock:stock-list-create")
    expected_data = RetrieveStockSerializer([stock, stock_extra], many=True).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = StockListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert "next" in response.data
    assert "previous" in response.data
    assert "count" in response.data
    assert response.data.get("results") == expected_data


@pytest.mark.django_db
def test_stock_list_create_view_post(rf, super_user, sector, sector_extra, stock_extra):
    factory = rf
    url = reverse("stock:stock-list-create")
    content = {"id": 2, "sector": 1}

    request = factory.post(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = StockListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("id", "sector") == content.get("id", "sector")
    assert "created", "updated" in response.data

@pytest.mark.django_db
def test_stock_retrieve_update_destroy_view_get(rf, sector, super_user, stock, stock_extra):
    factory = rf
    pk = 1
    url = reverse("stock:stock-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = RetrieveStockSerializer(stock).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = StockRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_stock_retrieve_update_destroy_view_put(rf, sector, sector_extra, super_user, stock):
    factory = rf
    pk = 1
    url = reverse("stock:stock-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = StockSerializer(stock).data.copy()
    expected_data["sector"] = 2

    content = {
        "sector": 2,
    }

    request = factory.put(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = StockRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_stock_retrieve_update_destroy_view_patch(rf, sector, sector_extra, super_user, stock):
    factory = rf
    pk = 1
    url = reverse("stock:stock-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = StockSerializer(stock).data.copy()
    expected_data["sector"] = 2

    content = {
        "sector": 2,
    }

    request = factory.patch(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = StockRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_all_sectors_views_get(rf, super_user, sector, sector_extra):
    factory = rf
    url = reverse("stock:all-sectors")
    expected_data = RetrieveSectorSerializer([sector_extra, sector], many=True).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = AllSectorsView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_sector_list_create_view_get(rf, super_user, sector, sector_extra):
    factory = rf
    url = reverse("stock:all-sectors")
    expected_data = RetrieveSectorSerializer([sector_extra, sector], many=True).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = SectorListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_200_OK
    assert "next" in response.data
    assert "previous" in response.data
    assert "count" in response.data
    assert response.data.get("results") == expected_data

@pytest.mark.django_db
def test_sector_list_create_view_post(rf, super_user, sector, public_defense, public_defense_extra):
    factory = rf
    url = reverse("stock:all-sectors")
    content = {"id": 2, "name": "Test Sector", "public_defense": 2}

    request = factory.post(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = SectorListCreateView.as_view()(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get("id", "public_defense") == content.get("id", "public_defense")
    assert "created", "updated" in response.data

@pytest.mark.django_db
def test_sector_retrieve_update_destroy_view_get(rf, super_user, sector, sector_extra):
    factory = rf
    pk = 1
    url = reverse("stock:sector-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = RetrieveSectorSerializer(sector).data

    request = factory.get(url)
    force_authenticate(request, user=super_user)
    response = SectorRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_sector_retrieve_update_destroy_view_put(rf, super_user, sector, public_defense, public_defense_extra):
    factory = rf
    pk = 1
    url = reverse("stock:sector-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = SectorSerializer(sector).data.copy()
    expected_data["name"] = "Test Sector Put"
    expected_data["public_defense"] = 2

    content = {
        "name": "Test Sector Put",
        "public_defense": 2,
    }

    request = factory.put(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = SectorRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.django_db
def test_sector_retrieve_update_destroy_view_patch(rf, super_user, sector, public_defense, public_defense_extra):
    factory = rf
    pk = 1
    url = reverse("stock:sector-retrieve-update-destroy", kwargs={"pk": pk})
    expected_data = SectorSerializer(sector).data.copy()
    expected_data["name"] = "Test Sector Patch"
    expected_data["public_defense"] = 2

    content = {
        "name": "Test Sector Patch",
        "public_defense": 2,
    }

    request = factory.patch(url, data=content, content_type="application/json")
    force_authenticate(request, user=super_user)
    response = SectorRetrieveUpdateDestroyView.as_view()(request, pk=pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data

@pytest.mark.skip
def test_all_public_defenses_view(rf, super_user, public_defense, public_defense_extra):
    factory = rf
    url = reverse()
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