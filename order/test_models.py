import pytest

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

@pytest.mark.django_db
def test_order(order):
    assert isinstance(order, Order)
    assert str(order) == f"Order {order.id}"

@pytest.mark.django_db
def test_order_item(order_item):
    assert isinstance(order_item, OrderItem)
    assert str(order_item) == f"order: {order_item.order.id} - {order_item.order.client.name} - {order_item.order.client.stock.sector.name} - {order_item.order.client.stock.sector.public_defense.name} - {order_item.product}"

@pytest.mark.django_db
def test_stock_with_drawal(stock_with_drawal):
    assert isinstance(stock_with_drawal, StockWithdrawal)
    assert str(stock_with_drawal) == f"StockWithdrawal {stock_with_drawal.id}"

@pytest.mark.django_db
def test_stock_entry(stock_entry):
    assert isinstance(stock_entry, StockEntry)
    assert str(stock_entry) == f"StockEntry {stock_entry.id}"

@pytest.mark.django_db
def test_supplier_order(supplier_oder):
    assert isinstance(supplier_oder, SupplierOrder)
    assert str(supplier_oder) == f"SupplierOrder {supplier_oder.id}"

@pytest.mark.django_db
def test_supplier_order_item(supplier_order_item):
    assert isinstance(supplier_order_item, SupplierOrderItem)
    assert str(supplier_order_item) == f"SupplierOrderItem {supplier_order_item.id}" 

@pytest.mark.django_db
def test_protocol_with_drawal(protocol_with_drawal):
    assert isinstance(protocol_with_drawal, ProtocolWithdrawal)
    assert str(protocol_with_drawal) == f"ProtocolWithdrawal {protocol_with_drawal.id}"

@pytest.mark.django_db
def test_materials_order(materials_order):
    assert isinstance(materials_order, MaterialsOrder)
    assert str(materials_order) == f"MaterialsOrder {materials_order.id}"

