import pytest
from django.contrib.auth.models import User
from datetime import date, datetime

from order.models import Order, OrderItem
from stock.models import (
    Category,
    Measure,
    Product,
    PublicDefense,
    Sector,
    Stock,
    StockItem,
    Supplier,
    DispatchReport,
    AccountantReport,
    CategoryBalance,
    Protocol,
    Invoice,
    ReceivingReport,
    BiddingExemption,
    ProtocolItem,
)
from user.models import Client


@pytest.fixture
def public_defense():
    return PublicDefense.objects.create(
        name="Test Public Defense", district="Test District", address="Test Address"
    )


@pytest.fixture
def sector(public_defense):
    return Sector.objects.create(name="Test Sector", public_defense=public_defense)


@pytest.fixture
def stock(sector):
    return Stock.objects.create(
        sector=sector,
    )


@pytest.fixture
def category(sector):
    category = Category.objects.create(name="Test Category", code="Test Code")
    category.sector.set([sector])
    return category


@pytest.fixture
def measure():
    return Measure.objects.create(name="Test Measure")


@pytest.fixture
def product(category, measure):
    return Product.objects.create(
        category=category,
        measure=measure,
        price=10.0,
        name="Test Product",
        description="Test Description",
        code="Test Code",
        is_available=True,
    )


@pytest.fixture
def stock_item(stock, product):
    return StockItem.objects.create(stock=stock, product=product, quantity=0)


@pytest.fixture
def supplier(category):
    supplier = Supplier.objects.create(
        name="Test Supplier",
        agent="Test Agent",
        address="Test Address",
        email="test@example.com",
        phone="1234567890",
        ein="12345",
        ssn="54321",
        nic="98765",
    )
    supplier.category.set([category])
    return supplier


@pytest.fixture
def protocol(supplier, category):
    return Protocol.objects.create(
        code="Test Code",
        supplier=supplier,
        category=category,
        start_date=datetime(2023, 6, 1, 10, 0, 0),
        end_date=datetime(2023, 6, 2, 15, 30, 0),
    )


@pytest.fixture
def protocol_item(protocol, product):
    return ProtocolItem.objects.create(
        protocol=protocol, product=product, original_quantity=0, quantity=0
    )


@pytest.fixture
def invoice(supplier, public_defense):
    return Invoice.objects.create(
        supplier=supplier,
        public_defense=public_defense,
        code="Test Code",
        total_value=10.00,
    )


@pytest.fixture
def receiving_report(product, stock_item, supplier):
    return ReceivingReport.objects.create(
        product=product,
        stock_item=stock_item,
        quantity=10,
        supplier=supplier,
        file="Test File",
        description="Test Description",
    )


@pytest.fixture
def dispatch_report(product, stock_item, public_defense):
    return DispatchReport.objects.create(
        product=product,
        stock_item=stock_item,
        quantity=0,
        public_defense=public_defense,
        file="Test File",
        description="Test Description",
    )


@pytest.fixture
def bidding_exemption(product, stock, invoice):
    return BiddingExemption.objects.create(
        product=product, stock=stock, invoice=invoice, quantity=0
    )


@pytest.fixture
def accountant_report():
    return AccountantReport.objects.create(
        month="June 2023",
        total_previous_value=1000.0,
        total_entry_value=500.0,
        total_output_value=200.0,
        total_current_value=1300.0,
    )


@pytest.fixture
def category_balance(category):
    return CategoryBalance.objects.create(
        category=category, date=date.today(), balance=1500.0
    )


@pytest.fixture
def client(stock):
    return Client.objects.create(
        user=User.objects.all().first(), name="test_client", stock=stock
    )


@pytest.fixture
def order(requester):
    return Order.objects.create(requester=requester)


@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(order=order, product=product)
