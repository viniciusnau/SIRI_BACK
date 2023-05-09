from django.urls import path

from .views import (
    AccountantReportListCreateView,
    AccountantReportRetrieveUpdateDestroyView,
    BiddingExemptionListCreateView,
    BiddingExemptionRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    DispatchReportListCreateView,
    DispatchReportRetrieveUpdateDestroyView,
    InvoiceListCreateView,
    InvoiceRetrieveUpdateDestroyView,
    MeasureListCreateView,
    MeasureRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProtocolItemListCreateView,
    ProtocolItemRetrieveUpdateDestroyView,
    ProtocolListCreateView,
    ProtocolRetrieveUpdateDestroyView,
    PublicDefenseListCreateView,
    PublicDefenseRetrieveUpdateDestroyView,
    ReceivingReportListCreateView,
    ReceivingReportRetrieveUpdateDestroyView,
    SectorListCreateView,
    SectorRetrieveUpdateDestroyView,
    StockItemListCreateView,
    StockItemRetrieveUpdateDestroyView,
    StockListCreateView,
    StockReport,
    StockRetrieveUpdateDestroyView,
    SupplierListCreateView,
    SupplierRetrieveUpdateDestroyView,
    WarehouseItems, EmailView,
)

app_name = "stock"

urlpatterns = [
    path("", StockListCreateView.as_view(), name="stock-list-create"),
    path(
        "<int:pk>/",
        StockRetrieveUpdateDestroyView.as_view(),
        name="stock-retrieve-update-destroy",
    ),
    path("sectors/", SectorListCreateView.as_view(), name="sector-list-create"),
    path(
        "sectors/<int:pk>/",
        SectorRetrieveUpdateDestroyView.as_view(),
        name="sector-retrieve-update-destroy",
    ),
    path("publicdefenses/", PublicDefenseListCreateView.as_view()),
    path("publicdefenses/<int:pk>/", PublicDefenseRetrieveUpdateDestroyView.as_view()),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path("measures/", MeasureListCreateView.as_view(), name="measure-list-create"),
    path(
        "measures/<int:pk>/",
        MeasureRetrieveUpdateDestroyView.as_view(),
        name="measure_retrieve_update_destroy",
    ),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-retrieve-update-destroy",
    ),
    path(
        "stock-items/", StockItemListCreateView.as_view(), name="stock-item-list-create"
    ),
    path(
        "stock-items/<int:pk>/",
        StockItemRetrieveUpdateDestroyView.as_view(),
        name="stock-item-detail",
    ),
    path("suppliers/", SupplierListCreateView.as_view(), name="supplier-list-create"),
    path(
        "suppliers/<int:pk>/",
        SupplierRetrieveUpdateDestroyView.as_view(),
        name="supplier-retrieve-update-destroy",
    ),
    path("protocols/", ProtocolListCreateView.as_view(), name="protocol-list-create"),
    path(
        "protocols/<int:pk>/",
        ProtocolRetrieveUpdateDestroyView.as_view(),
        name="protocol-retrieve-update-destroy",
    ),
    path(
        "protocol-items/",
        ProtocolItemListCreateView.as_view(),
        name="protocol-item-list-create",
    ),
    path(
        "protocol-items/<int:pk>/",
        ProtocolItemRetrieveUpdateDestroyView.as_view(),
        name="protocol-item-retrieve-update-destroy",
    ),
    path("invoices/", InvoiceListCreateView.as_view(), name="invoice-list-create"),
    path(
        "invoices/<int:pk>/",
        InvoiceRetrieveUpdateDestroyView.as_view(),
        name="invoice-retrieve-update-destroy",
    ),
    path(
        "receiving-reports/",
        ReceivingReportListCreateView.as_view(),
        name="receiving_report_list_create",
    ),
    path(
        "receiving-reports/<int:pk>/",
        ReceivingReportRetrieveUpdateDestroyView.as_view(),
        name="receiving_report_retrieve_update_destroy",
    ),
    path(
        "dispatch-reports/",
        DispatchReportListCreateView.as_view(),
        name="dispatch_report_list_create",
    ),
    path(
        "dispatch-reports/<int:pk>/",
        DispatchReportRetrieveUpdateDestroyView.as_view(),
        name="dispatch_report_retrieve_update_destroy",
    ),
    path(
        "bidding-exemption/",
        BiddingExemptionListCreateView.as_view(),
        name="bidding_exemption_list_create",
    ),
    path(
        "biddings-exemption/<int:pk>/",
        BiddingExemptionRetrieveUpdateDestroyView.as_view(),
        name="bidding_exemption_retrieve_update_destroy",
    ),
    path(
        "accountant-reports/",
        AccountantReportListCreateView.as_view(),
        name="accountant_report_list_create",
    ),
    path(
        "accountant-reports/<int:pk>/",
        AccountantReportRetrieveUpdateDestroyView.as_view(),
        name="accountant_report_retrieve_update_destroy",
    ),
    path("stock-report/", StockReport.as_view(), name="stock_report"),
    path("warehouse-items/", WarehouseItems.as_view(), name="warehouse_items"),
    path('email/', EmailView.as_view()),
]
