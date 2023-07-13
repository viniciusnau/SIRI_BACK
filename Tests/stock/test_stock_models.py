import pytest

from stock.models import (
    AccountantReport,
    BiddingExemption,
    Category,
    CategoryBalance,
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


@pytest.mark.django_db
def test_public_defense(public_defense):
    assert isinstance(public_defense, PublicDefense)
    assert public_defense.id == 1
    assert str(public_defense) == "Test Public Defense"


@pytest.mark.django_db
def test_sector(sector):
    assert isinstance(sector, Sector)
    assert str(sector) == "Test Sector"


@pytest.mark.django_db
def test_stock(stock):
    assert isinstance(stock, Stock)
    assert stock.id == 1
    assert str(stock) == f"{stock.sector} - {stock.sector.public_defense}"


@pytest.mark.django_db
def test_category(category):
    assert isinstance(category, Category)
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_measure(measure):
    assert isinstance(measure, Measure)
    assert str(measure) == "Test Measure"


@pytest.mark.django_db
def test_product(product):
    assert isinstance(product, Product)
    assert str(product) == "Test Product"


@pytest.mark.django_db
def test_stock_item(stock_item):
    assert isinstance(stock_item, StockItem)
    assert (
        str(stock_item)
        == f"{stock_item.stock.sector} - {stock_item.stock.sector.public_defense} - {stock_item.product}"
    )


@pytest.mark.django_db
def test_supplier(supplier):
    assert isinstance(supplier, Supplier)
    assert str(supplier) == "Test Supplier"


@pytest.mark.django_db
def test_protocol(protocol):
    assert isinstance(protocol, Protocol)
    assert str(protocol) == "Test Code"


@pytest.mark.django_db
def test_protocol_item(protocol_item):
    assert isinstance(protocol_item, ProtocolItem)
    assert (
        str(protocol_item)
        == f"{protocol_item.protocol} - {protocol_item.protocol.supplier} - {protocol_item.product}"
    )


@pytest.mark.django_db
def test_invoice(invoice):
    assert isinstance(invoice, Invoice)
    assert str(invoice) == "Test Code"


@pytest.mark.django_db
def test_receiving_report(receiving_report):
    assert isinstance(receiving_report, ReceivingReport)
    assert str(receiving_report) == f"ReceivingReport {receiving_report.id}"


@pytest.mark.django_db
def test_dispatch_report(dispatch_report):
    assert isinstance(dispatch_report, DispatchReport)
    assert str(dispatch_report) == f"DispatchReport {dispatch_report.id}"


@pytest.mark.django_db
def test_bidding_exemption(bidding_exemption):
    assert isinstance(bidding_exemption, BiddingExemption)
    assert str(bidding_exemption) == f"BiddingExemption {bidding_exemption.id}"


@pytest.mark.django_db
def test_accountant_report(accountant_report):
    assert isinstance(accountant_report, AccountantReport)
    assert str(accountant_report) == f"AccountantReport {accountant_report.id}"


@pytest.mark.django_db
def test_category_balance(category_balance):
    assert isinstance(category_balance, CategoryBalance)
    assert str(category_balance) == f"CategoryBalance {category_balance.id}"
