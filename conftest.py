import pytest
from django.contrib.auth.models import User

from order.models import Order, OrderItem
from stock.models import (
    Category,
    Measure,
    Product,
    PublicDefense,
    Sector,
    Stock,
    StockItem,
)
from user.models import Client


@pytest.fixture
def measure():
    return Measure.objects.create(name="test_measure")


@pytest.fixture
def public_defense():
    return PublicDefense.objects.create(
        name="test_public_defense", district="test_district", address="test_address"
    )


@pytest.fixture
def sector(public_defense):
    return Sector.objects.create(name="test_sector", public_defense=public_defense)


@pytest.fixture
def category(sector):
    category = Category.objects.create(
        name="test_category", slug="test_category_slug", is_standard=True
    )
    category.sector.add(sector)
    return category


@pytest.fixture
def product(category, measure):
    return Product.objects.create(
        category=category,
        measure=measure,
        name="test_product",
        slug="test_product_slug",
    )


@pytest.fixture
def stock(sector):
    return Stock.objects.create(sector=sector)


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


@pytest.fixture
def stock_item(stock, product):
    return StockItem.objects.create(stock=stock, product=product, current_quantity=2)
