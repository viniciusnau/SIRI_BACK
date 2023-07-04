import pytest
import datetime
from decimal import Decimal

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
        "id": sector.id,
        "name": sector.name,
        "public_defense": PublicDefenseSerializer(sector.public_defense).data,
        "created": sector.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": sector.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_sector_serializer(sector):
    serializer = SectorSerializer(sector)
    expected_data = {
        "id": sector.id,
        "name": sector.name,
        "public_defense": sector.public_defense.id,
        "created": sector.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": sector.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_category_serializer(category):
    serializer = CategorySerializer(category)
    expected_data = {
        "id": category.id,
        "name": category.name,
        "code": category.code,
    }

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_measure_serializer(measure):
    serializer = MeasureSerializer(measure)
    expected_data = {
        "id": measure.id,
        "name": measure.name,
        "created": measure.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": measure.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_retrieve_product_serializer(product):
    serializer = RetrieveProductSerializer(product)
    expected_data = {
        "id": product.id,
        "category": CategorySerializer(product.category).data,
        "measure": MeasureSerializer(product.measure).data,
        "price": product.price,
        "name": product.name,
        "description": product.description,
        "code": product.code,
        "is_available": product.is_available,
        "created": product.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": product.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_product_serializer(product):
    serializer = ProductSerializer(product)
    expected_data = {
        "id": product.id,
        "category": product.category.id,
        "measure": product.measure.id,
        "price": product.price,
        "name": product.name,
        "description": product.description,
        "code": product.code,
        "is_available": product.is_available,
        "created": product.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": product.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_measure_name_serializer(measure):
    serializer = MeasureNameSerializer(measure)
    expected_data = {
        "name": measure.name
    }
    assert serializer.data == expected_data
@pytest.mark.django_db
def test_product_me_serializer(product):
    serializer = ProductMeSerializer(product)
    expected_data = {
        "id": product.id,
        "name": product.name,
        "measure": MeasureNameSerializer(product.measure).data,
        "description": product.description,
    }
    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_stock_item_serializer(stock_item):
    serializer = RetrieveStockItemSerializer(stock_item)
    obj = stock_item
    expected_data = {
        "id": stock_item.id,
        "stock": RetrieveStockSerializer(stock_item.stock).data,
        "product": ProductMeSerializer(stock_item.product).data,
        "quantity": stock_item.quantity,
        "created": stock_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": stock_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_stock(obj) == RetrieveStockSerializer(obj.stock).data
@pytest.mark.django_db
def test_stock_item_serializer(stock_item):
    serializer = StockItemSerializer(stock_item)
    expected_data = {
        "id": stock_item.id,
        "stock": stock_item.stock.id,
        "product": stock_item.product.id,
        "quantity": stock_item.quantity,
        "created": stock_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": stock_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_stock_item_me_serializer(stock_item):
    serializer = StockItemMeSerializer(stock_item)
    expected_data = {
        "id": stock_item.id,
        "product": ProductMeSerializer(stock_item.product).data,
        "quantity": stock_item.quantity,
        "created": stock_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": stock_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data


@pytest.mark.django_db
def test_retrieve_supplier_serializer(supplier):
    serializer = RetrieveSupplierSerializer(supplier)
    expected_data = {
        "id": supplier.id,
        "name": supplier.name,
        "agent": supplier.agent,
        "category": CategorySerializer(supplier.category.all(), many=True).data,
        "address": supplier.address,
        "email": supplier.email,
        "phone": supplier.phone,
        "ein": supplier.ein,
        "ssn": supplier.ssn,
        "nic": supplier.nic,
        "created": supplier.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": supplier.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_supplier_serializer(supplier):
    serializer = SupplierSerializer(supplier)
    expected_data = {
        "id": supplier.id,
        "name": supplier.name,
        "agent": supplier.agent,
        "category": [category.id for category in supplier.category.all()],
        "address": supplier.address,
        "email": supplier.email,
        "phone": supplier.phone,
        "ein": supplier.ein,
        "ssn": supplier.ssn,
        "nic": supplier.nic,
        "created": supplier.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": supplier.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_supplier_name_serializer(supplier):
    serializer = SupplierNameSerializer(supplier)
    expected_data = {
        "id": supplier.id,
        "name": supplier.name,
    }
    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_protocol_serializer(protocol, monkeypatch):
    serializer = RetrieveProtocolSerializer(protocol)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{protocol.code}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)

    expected_data = {
        "id": protocol.id,
        "code": protocol.code,
        "start_date": protocol.start_date.replace(microsecond=0).isoformat() + "Z",
        "end_date": protocol.end_date.replace(microsecond=0).isoformat() + "Z",
        "supplier": SupplierNameSerializer(protocol.supplier).data,
        "category": CategorySerializer(protocol.category).data,
        "file": expected_url,
    }

    assert serializer.data == expected_data
    assert serializer.get_file(protocol) == expected_url


@pytest.mark.django_db
def test_protocol_serializer(protocol, monkeypatch):
    serializer = ProtocolSerializer(protocol)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{protocol.code}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)

    expected_data = {
        "id": protocol.id,
        "code": protocol.code,
        "start_date": protocol.start_date.replace(microsecond=0).isoformat() + "Z",
        "end_date": protocol.end_date.replace(microsecond=0).isoformat() + "Z",
        "supplier": protocol.supplier.id,
        "category": protocol.category.id,
        "file": expected_url,
    }

    assert serializer.data == expected_data
    assert serializer.get_file(protocol) == expected_url

@pytest.mark.django_db
def test_protocol_code_serializer(protocol):
    serializer = ProtocolCodeSerializer(protocol)
    expected_data = {
        "id": protocol.id,
        "code": protocol.code,
    }
    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_protocol_item_serializer(protocol_item):
    serializer = RetrieveProtocolItemSerializer(protocol_item)
    expected_data = {
        "id": protocol_item.id,
        "protocol": protocol_item.protocol.id,
        "product": ProductMeSerializer(protocol_item.product).data,
        "original_quantity": protocol_item.original_quantity,
        "quantity": protocol_item.quantity,
        "created": protocol_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": protocol_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
@pytest.mark.django_db
def test_protocol_item_serializer(protocol_item):
    serializer = ProtocolItemSerializer(protocol_item)
    expected_data = {
        "id": protocol_item.id,
        "protocol": protocol_item.protocol.id,
        "product":  protocol_item.product.id,
        "original_quantity": protocol_item.original_quantity,
        "quantity": protocol_item.quantity,
        "created": protocol_item.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": protocol_item.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_invoice_serializer(invoice, monkeypatch):
    serializer = RetrieveInvoiceSerializer(invoice)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{invoice.code}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": invoice.id,
        "total_value": str(Decimal(str(invoice.total_value)).quantize(Decimal("0.00"))),
        "public_defense": PublicDefenseSerializer(invoice.public_defense).data,
        "supplier": SupplierNameSerializer(invoice.supplier).data,
        "file": expected_url,
        "code": invoice.code,
        "created": invoice.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": invoice.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(invoice) == expected_url

@pytest.mark.django_db
def test_invoice_serializer(invoice, monkeypatch):
    serializer = InvoiceSerializer(invoice)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{invoice.code}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": invoice.id,
        "total_value": f"{invoice.total_value:.2f}",
        "public_defense": invoice.public_defense.id,
        "supplier": invoice.supplier.id,
        "file": expected_url,
        "code": invoice.code,
        "created": invoice.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": invoice.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(invoice) == expected_url

@pytest.mark.django_db
def test_retrieve_receiving_report_serializer(receiving_report, monkeypatch):
    serializer = RetrieveReceivingReportSerializer(receiving_report)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{receiving_report.id}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": receiving_report.id,
        "product": ProductMeSerializer(receiving_report.product).data,
        "quantity": receiving_report.quantity,
        "supplier": SupplierNameSerializer(receiving_report.supplier).data,
        "file": expected_url,
        "description": receiving_report.description,
        "created": receiving_report.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": receiving_report.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(receiving_report) == expected_url

@pytest.mark.django_db
def test_receiving_report_serializer(receiving_report, monkeypatch):
    serializer = ReceivingReportSerializer(receiving_report)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{receiving_report.id}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": receiving_report.id,
        "product": receiving_report.product.id,
        "quantity": receiving_report.quantity,
        "supplier": receiving_report.supplier.id,
        "file": expected_url,
        "description": receiving_report.description,
        "created": receiving_report.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": receiving_report.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(receiving_report) == expected_url

@pytest.mark.django_db
def test_retrieve_dispatch_report_serializer(dispatch_report, monkeypatch):
    serializer = RetrieveDispatchReportSerializer(dispatch_report)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{dispatch_report.id}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": dispatch_report.id,
        "product": ProductMeSerializer(dispatch_report.product).data,
        "quantity": dispatch_report.quantity,
        "public_defense": PublicDefenseSerializer(dispatch_report.public_defense).data,
        "file": expected_url,
        "description": dispatch_report.description,
        "created": dispatch_report.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": dispatch_report.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(dispatch_report) == expected_url
@pytest.mark.django_db
def test_dispatch_report_serializer(dispatch_report, monkeypatch):
    serializer = DispatchReportSerializer(dispatch_report)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{dispatch_report.id}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": dispatch_report.id,
        "product": dispatch_report.product.id,
        "quantity": dispatch_report.quantity,
        "public_defense": dispatch_report.public_defense.id,
        "file": expected_url,
        "description": dispatch_report.description,
        "created": dispatch_report.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": dispatch_report.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data
    assert serializer.get_file(dispatch_report) == expected_url

@pytest.mark.django_db
def test_invoice_code_serializer(invoice):
    serializer = InvoiceCodeSerializer(invoice)
    expected_data = {
        "id": invoice.id,
        "code": invoice.code,
    }
    assert serializer.data == expected_data

@pytest.mark.django_db
def test_retrieve_bidding_exemption_serializer(bidding_exemption):
    serializer = RetrieveBiddingExemptionSerializer(bidding_exemption)
    expected_data = {
        "id": bidding_exemption.id,
        "product": ProductMeSerializer(bidding_exemption.product).data,
        "stock": bidding_exemption.stock.id,
        "invoice": InvoiceCodeSerializer(bidding_exemption.invoice).data,
        "quantity": bidding_exemption.quantity,
        "created": bidding_exemption.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": bidding_exemption.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_bidding_exemption_serializer(bidding_exemption):
    serializer = BiddingExemptionSerializer(bidding_exemption)
    expected_data = {
        "id": bidding_exemption.id,
        "product": bidding_exemption.product.id,
        "stock": bidding_exemption.stock.id,
        "invoice": bidding_exemption.invoice.id,
        "quantity": bidding_exemption.quantity,
        "created": bidding_exemption.created.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "updated": bidding_exemption.updated.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
    }
    expected_data["created"] = expected_data["created"].replace("+0000", "Z")
    expected_data["updated"] = expected_data["updated"].replace("+0000", "Z")

    assert serializer.data == expected_data

@pytest.mark.django_db
def test_accountant_report_serializer(accountant_report, monkeypatch):
    serializer = AccountantReportSerializer(accountant_report)
    expected_url = f"https://local-sed.s3.amazonaws.com/protocols/{accountant_report.month}?AWSAccessKeyId=AKIA23MFNYI3HNN4N4ZT&Signature=HMoGyIfsTDkOtq2u3klQnPoPbBI%3D&Expires=1688495698"

    def mock_generate_presigned_url(*args, **kwargs):
        return expected_url

    monkeypatch.setattr(serializer, 'get_file', mock_generate_presigned_url)
    expected_data = {
        "id": accountant_report.id,
        "month": accountant_report.month,
        "total_previous_value": accountant_report.total_previous_value,
        "total_entry_value": accountant_report.total_entry_value,
        "total_output_value": accountant_report.total_output_value,
        "total_current_value": accountant_report.total_current_value,
        "file": expected_url,
    }
    assert serializer.data == expected_data
    assert serializer.get_file(accountant_report) == expected_url

@pytest.mark.skip
def test_accountant_report_category_serializer():
    pass

@pytest.mark.skip
def test_email_serializer():
    pass
