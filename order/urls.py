from django.urls import path

from .views import (
    AllOrderItemsView,
    MaterialsOrderListCreateView,
    MaterialsOrderRetrieveUpdateDestroyView,
    OrderItemListCreateView,
    OrderItemRetrieveUpdateDestroyView,
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    ProtocolWithdrawalListCreateView,
    ProtocolWithdrawalRetrieveUpdateDestroyView,
    StockEntryListCreateView,
    StockEntryRetrieveUpdateDestroyView,
    StockWithdrawalListCreateView,
    StockWithdrawalRetrieveUpdateDestroyView,
    SupplierOrderItemListCreateView,
    SupplierOrderItemRetrieveUpdateDestroyView,
    SupplierOrderListCreateView,
    SupplierOrderRetrieveUpdateDestroyView,
)

app_name = "order"

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "<int:pk>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
    path(
        "order-items/", OrderItemListCreateView.as_view(), name="order-item-list-create"
    ),
    path("order-items/all/", AllOrderItemsView.as_view(), name="all-order-items"),
    path(
        "order-items/<int:pk>/",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="order-item-retrieve-update-destroy",
    ),
    path(
        "stock-withdrawals/",
        StockWithdrawalListCreateView.as_view(),
        name="stock-withdrawal-list-create",
    ),
    path(
        "stock-withdrawals/<int:pk>/",
        StockWithdrawalRetrieveUpdateDestroyView.as_view(),
        name="stock-withdrawal-retrieve-update-destroy",
    ),
    path("stock-entries/", StockEntryListCreateView.as_view(), name="stock-entry-list"),
    path(
        "stock-entries/<int:pk>/",
        StockEntryRetrieveUpdateDestroyView.as_view(),
        name="stock-entry-detail",
    ),
    path(
        "supplier-orders/",
        SupplierOrderListCreateView.as_view(),
        name="supplier-order-list-create",
    ),
    path(
        "supplier-orders/<int:pk>/",
        SupplierOrderRetrieveUpdateDestroyView.as_view(),
        name="supplier-order-retrieve-update-destroy",
    ),
    path(
        "supplier-order-items/",
        SupplierOrderItemListCreateView.as_view(),
        name="supplier-order-item-list-create",
    ),
    path(
        "supplier-order-items/<int:pk>/",
        SupplierOrderItemRetrieveUpdateDestroyView.as_view(),
        name="supplier-order-item-retrieve-update-destroy",
    ),
    path(
        "protocol-withdrawals/",
        ProtocolWithdrawalListCreateView.as_view(),
        name="protocol-withdrawal-list-create",
    ),
    path(
        "protocol-withdrawals/<int:pk>/",
        ProtocolWithdrawalRetrieveUpdateDestroyView.as_view(),
        name="protocol-withdrawal-retrieve-update-destroy",
    ),
    path(
        "materials-order/",
        MaterialsOrderListCreateView.as_view(),
        name="materials-order-list-create",
    ),
    path(
        "materials-order/<int:pk>/",
        MaterialsOrderRetrieveUpdateDestroyView.as_view(),
        name="materials-order-retrieve-update-destroy",
    ),
]
