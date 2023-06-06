import os
import tempfile
from datetime import datetime
from decimal import Decimal

import boto3
from django.core.mail import EmailMultiAlternatives
from django.db.models import F, FloatField, Q, Sum
from django.db.models.functions import Cast
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import StockEntry, StockWithdrawal
from user.models import Client

from .models import (
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
from .serializers import (
    AccountantReportCategorySerializer,
    AccountantReportSerializer,
    BiddingExemptionSerializer,
    CategorySerializer,
    DispatchReportSerializer,
    EmailSerializer,
    InvoiceSerializer,
    MeasureSerializer,
    ProductSerializer,
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
    StockItemSerializer,
    StockSerializer,
    SupplierSerializer,
)
from .services import get_protocol_item_quantity, get_stock_item_quantity

client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION_NAME"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = RetrieveStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockSerializer
        elif self.request.method in ["POST"]:
            return StockSerializer


class StockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return StockSerializer


class SectorListCreateView(generics.ListCreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = RetrieveSectorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSectorSerializer
        elif self.request.method in ["POST"]:
            return SectorSerializer


class SectorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSectorSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return SectorSerializer


class PublicDefenseListCreateView(generics.ListCreateAPIView):
    queryset = PublicDefense.objects.all()
    serializer_class = PublicDefenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class PublicDefenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PublicDefense.objects.all()
    serializer_class = PublicDefenseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasureListCreateView(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = RetrieveProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        category_ids = self.request.query_params.get("category_id")
        if category_ids:
            category_ids = [int(category_id) for category_id in category_ids.split(",")]
            queryset = queryset.filter(category__id__in=category_ids)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProductSerializer
        elif self.request.method in ["POST"]:
            return ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProductSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return ProductSerializer


class StockItemListCreateView(generics.ListCreateAPIView):
    serializer_class = RetrieveStockItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        stock_ids = self.request.query_params.get("stock_id")
        if stock_ids:
            stock_ids = [int(stock_id) for stock_id in stock_ids.split(",")]
            queryset = StockItem.objects.filter(stock__id__in=stock_ids)
        else:
            queryset = StockItem.objects.all()
        for stock_item in queryset:
            if stock_item.stock.id != 1:
                stock_item.quantity = get_stock_item_quantity(stock_item)
                stock_item.save(update_fields=["quantity"])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockItemSerializer
        elif self.request.method in ["POST"]:
            return StockItemSerializer


class StockItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.stock.id != 1:
            instance.quantity = get_stock_item_quantity(instance)
            instance.save(update_fields=["quantity"])
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.stock.id != 1:
            instance.quantity = get_stock_item_quantity(instance)
        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockItemSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return StockItemSerializer


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = RetrieveSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSupplierSerializer
        elif self.request.method in ["POST"]:
            return SupplierSerializer


class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = RetrieveSupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSupplierSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return SupplierSerializer


class ProtocolListCreateView(generics.ListCreateAPIView):
    queryset = Protocol.objects.all()
    serializer_class = RetrieveProtocolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        file_data = self.request.data.get("file")
        code = self.request.data.get("code")

        with tempfile.TemporaryFile() as tmp_file:
            for chunk in file_data.file:
                tmp_file.write(chunk)
            tmp_file.seek(0)
            client.upload_fileobj(
                tmp_file, os.environ.get("AWS_BUCKET_NAME"), f"protocols/{code}"
            )
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProtocolSerializer
        elif self.request.method in ["POST"]:
            return ProtocolSerializer


class ProtocolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Protocol.objects.all()
    serializer_class = RetrieveProtocolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProtocolSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return ProtocolSerializer

    def perform_update(self, serializer):
        file_data = self.request.data.get("file")
        code = self.request.data.get("code")

        if file_data:
            with tempfile.TemporaryFile() as tmp_file:
                for chunk in file_data.file:
                    tmp_file.write(chunk)
                tmp_file.seek(0)
                file_path = f"protocols/{code}"
                client.upload_fileobj(
                    tmp_file, os.environ.get("AWS_BUCKET_NAME"), file_path
                )

        serializer.save()

class ProtocolItemListCreateView(generics.ListCreateAPIView):
    queryset = ProtocolItem.objects.all()
    serializer_class = RetrieveProtocolItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        protocol_ids = self.request.query_params.get("protocol_id")
        if protocol_ids:
            protocol_ids = protocol_ids.split(",")
            queryset = queryset.filter(protocol__id__in=protocol_ids)
        for protocol_item in queryset:
            protocol_item.quantity = get_protocol_item_quantity(protocol_item)
            protocol_item.save(update_fields=["quantity"])
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProtocolItemSerializer
        elif self.request.method in ["POST"]:
            return ProtocolItemSerializer


class ProtocolItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProtocolItem.objects.all()
    serializer_class = RetrieveProtocolItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.quantity = get_protocol_item_quantity(instance)
        instance.save(update_fields=["quantity"])
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProtocolItemSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return ProtocolItemSerializer


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = RetrieveInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier_ids = self.request.query_params.get("supplier_id")
        if supplier_ids:
            supplier_ids = supplier_ids.split(",")
            queryset = queryset.filter(supplier__id__in=supplier_ids)

        public_defense_id = self.request.query_params.get("public_defense_id")
        if public_defense_id:
            queryset = queryset.filter(public_defense__id=public_defense_id)

        return queryset

    def perform_create(self, serializer):
        file_data = self.request.data.get("file")
        code = self.request.data.get("code")

        with tempfile.TemporaryFile() as tmp_file:
            for chunk in file_data.file:
                tmp_file.write(chunk)
            tmp_file.seek(0)
            client.upload_fileobj(
                tmp_file, os.environ.get("AWS_BUCKET_NAME"), f"invoices/{code}"
            )
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveInvoiceSerializer
        elif self.request.method in ["POST"]:
            return InvoiceSerializer


class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = RetrieveInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveInvoiceSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return InvoiceSerializer


class ReceivingReportListCreateView(generics.ListCreateAPIView):
    queryset = ReceivingReport.objects.all()
    serializer_class = RetrieveReceivingReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveReceivingReportSerializer
        elif self.request.method in ["POST"]:
            return ReceivingReportSerializer


class ReceivingReportRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReceivingReport.objects.all()
    serializer_class = RetrieveReceivingReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        file_data = self.request.data.get("file")
        if file_data:
            client.upload_fileobj(
                file_data,
                os.environ.get("AWS_BUCKET_NAME"),
                f"receiving-reports/{instance.id}",
            )
            instance.file = str(instance.id)
        instance.description = self.request.data.get("description")
        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveReceivingReportSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return ReceivingReportSerializer


class DispatchReportListCreateView(generics.ListCreateAPIView):
    queryset = DispatchReport.objects.all()
    serializer_class = RetrieveDispatchReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveDispatchReportSerializer
        elif self.request.method in ["POST"]:
            return DispatchReportSerializer


class DispatchReportRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DispatchReport.objects.all()
    serializer_class = RetrieveDispatchReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        file_data = self.request.data.get("file")
        client.upload_fileobj(
            file_data,
            os.environ.get("AWS_BUCKET_NAME"),
            f"dispatch-reports/{instance.id}",
        )
        instance.file = str(instance.id)
        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveDispatchReportSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return DispatchReportSerializer


class BiddingExemptionListCreateView(generics.ListCreateAPIView):
    queryset = BiddingExemption.objects.all()
    serializer_class = RetrieveBiddingExemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        stock = Stock.objects.get(id=int(self.request.data.get("stock")))
        warehouse = Stock.objects.get(id=1)
        product = Product.objects.get(id=int(self.request.data.get("product")))
        invoice = Invoice.objects.get(id=int(self.request.data.get("invoice")))
        quantity = int(self.request.data.get("quantity"))

        if stock.id != warehouse.id:
            stock_item, created = StockItem.objects.get_or_create(
                product=product, stock=stock
            )
            StockEntry.objects.create(stock_item=stock_item, entry_quantity=quantity)
            ReceivingReport.objects.create(
                product=product, supplier=invoice.supplier, quantity=quantity
            )
            warehouse_stock_item, created = StockItem.objects.get_or_create(
                product=product, stock=warehouse
            )
            warehouse_stock_item.quantity = warehouse_stock_item.quantity + quantity
            warehouse_stock_item.save(update_fields=["quantity"])
            DispatchReport.objects.create(
                public_defense=stock.sector.public_defense,
                product=product,
                quantity=quantity,
            )
            warehouse_stock_item = StockItem.objects.get(id=warehouse_stock_item.id)
            warehouse_stock_item.quantity = warehouse_stock_item.quantity - quantity
            warehouse_stock_item.save(update_fields=["quantity"])
        else:
            stock_item, created = StockItem.objects.get_or_create(
                product=product, stock=warehouse
            )
            stock_item.quantity = stock_item.quantity + quantity
            stock_item.save(update_fields=["quantity"])
            ReceivingReport.objects.create(
                product=product, supplier=invoice.supplier, quantity=quantity
            )

        serializer.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveBiddingExemptionSerializer
        elif self.request.method in ["POST"]:
            return BiddingExemptionSerializer


class BiddingExemptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BiddingExemption.objects.all()
    serializer_class = BiddingExemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveBiddingExemptionSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return BiddingExemptionSerializer


class AccountantReportListCreateView(generics.ListCreateAPIView):
    queryset = AccountantReport.objects.all()
    serializer_class = AccountantReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        date = request.query_params.get("date")
        if not date:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        month = date.split("-")[0]
        year = date.split("-")[1]
        date = datetime(int(year), int(month), 1).date()

        receiving_reports = ReceivingReport.objects.filter(
            created__month=month, created__year=year
        ).select_related("product")

        categories = receiving_reports.values(
            "product__category__name", "product__category__code"
        ).annotate(
            entry_value=Sum(
                F("product__price") * F("quantity"), output_field=FloatField()
            )
        )

        dispatch_reports = DispatchReport.objects.filter(
            created__month=month, created__year=year
        ).select_related("product")

        dispatch_categories = dispatch_reports.values(
            "product__category__name", "product__category__code"
        ).annotate(
            output_value=Sum("quantity", output_field=FloatField())
            * F("product__price")
        )

        for category in categories:
            dispatch_category = dispatch_categories.filter(
                product__category__name=category["product__category__name"],
                product__category__code=category["product__category__code"],
            )
            if dispatch_category:
                category["output_value"] = dispatch_category.aggregate(
                    Sum("output_value")
                )["output_value__sum"]
            else:
                category["output_value"] = 0.00

            category["balance"] = category["entry_value"] - category["output_value"]
            category_obj = Category.objects.get(
                code=category["product__category__code"]
            )
            category_balance, _ = CategoryBalance.objects.update_or_create(
                category=category_obj, date=date, balance=category["balance"]
            )
            previous_balance = (
                CategoryBalance.objects.exclude(
                    category=category_obj, date=date, balance=category["balance"]
                )
                .exclude(date__gte=date)
                .aggregate(Sum("balance"))["balance__sum"]
            )
            if not previous_balance:
                previous_balance = Decimal(0.00)
            category["previous_balance"] = previous_balance
            category["current_balance"] = previous_balance + Decimal(
                category["balance"]
            )

        serializer = AccountantReportCategorySerializer(categories, many=True)
        return Response(
            {
                "categories": serializer.data,
            }
        )

    def perform_create(self, serializer):
        file_data = self.request.data.get("file")
        month = self.request.data.get("month")

        with tempfile.TemporaryFile() as tmp_file:
            for chunk in file_data.file:
                tmp_file.write(chunk)
            tmp_file.seek(0)
            client.upload_fileobj(
                tmp_file,
                os.environ.get("AWS_BUCKET_NAME"),
                f"accountant-reports/{month}",
            )
        serializer.save()


class AccountantReportRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccountantReport.objects.all()
    serializer_class = AccountantReportSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockReport(APIView):
    def get(self, request, *args, **kwargs):
        initial_date = request.query_params.get("initial_date")
        final_date = request.query_params.get("final_date")
        initial_date = datetime.strptime(initial_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        final_date = datetime.strptime(final_date, "%d/%m/%Y").strftime("%Y-%m-%d")
        product_ids = request.query_params.getlist("product")
        public_defense_ids = request.query_params.getlist("public_defense")
        sector_ids = request.query_params.getlist("sector")
        categories = request.query_params.getlist("category")
        response = []

        if product_ids:
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                if categories:
                    if str(product.category_id) in categories:
                        if public_defense_ids:
                            for public_defense_id in public_defense_ids:
                                public_defense = PublicDefense.objects.get(
                                    id=public_defense_id
                                )
                                entry_filters = Q(
                                    entry_date__gte=initial_date,
                                    entry_date__lte=final_date,
                                )
                                entry_filters &= Q(stock_item__product_id=product_id)
                                entry_filters &= Q(
                                    stock_item__stock__sector__public_defense_id=public_defense_id
                                )
                                entry_filters &= ~Q(stock_item__stock_id=1)
                                entry_quantity = (
                                    StockEntry.objects.filter(entry_filters).aggregate(
                                        Sum("entry_quantity")
                                    )["entry_quantity__sum"]
                                    or 0
                                )
                                entry_price = product.price * entry_quantity

                                withdraw_filters = Q(
                                    withdraw_date__gte=initial_date,
                                    withdraw_date__lte=final_date,
                                )
                                withdraw_filters &= Q(stock_item__product_id=product_id)
                                withdraw_filters &= Q(
                                    stock_item__stock__sector__public_defense_id=public_defense_id
                                )
                                withdraw_filters &= ~Q(stock_item__stock_id=1)
                                withdrawal_quantity = (
                                    StockWithdrawal.objects.filter(
                                        withdraw_filters
                                    ).aggregate(Sum("withdraw_quantity"))[
                                        "withdraw_quantity__sum"
                                    ]
                                    or 0
                                )
                                withdrawal_price = product.price * withdrawal_quantity

                                response.append(
                                    {
                                        "public_defense": public_defense.name,
                                        "product_code": product.code,
                                        "product_name": product.name,
                                        "entry_quantity": entry_quantity,
                                        "withdrawal_quantity": withdrawal_quantity,
                                        "entry_price": entry_price,
                                        "withdrawal_price": withdrawal_price,
                                    }
                                )
                        else:
                            for sector_id in sector_ids:
                                sector = Sector.objects.get(id=sector_id)
                                entry_filters = Q(
                                    entry_date__gte=initial_date,
                                    entry_date__lte=final_date,
                                )
                                entry_filters &= Q(stock_item__product_id=product_id)
                                entry_filters &= Q(
                                    stock_item__stock__sector_id=sector_id
                                )
                                entry_filters &= ~Q(stock_item__stock_id=1)
                                entry_quantity = (
                                    StockEntry.objects.filter(entry_filters).aggregate(
                                        Sum("entry_quantity")
                                    )["entry_quantity__sum"]
                                    or 0
                                )
                                entry_price = product.price * entry_quantity

                                withdraw_filters = Q(
                                    withdraw_date__gte=initial_date,
                                    withdraw_date__lte=final_date,
                                )
                                withdraw_filters &= Q(stock_item__product_id=product_id)
                                withdraw_filters &= Q(
                                    stock_item__stock__sector_id=sector_id
                                )
                                withdraw_filters &= ~Q(stock_item__stock_id=1)
                                withdrawal_quantity = (
                                    StockWithdrawal.objects.filter(
                                        withdraw_filters
                                    ).aggregate(Sum("withdraw_quantity"))[
                                        "withdraw_quantity__sum"
                                    ]
                                    or 0
                                )
                                withdrawal_price = product.price * withdrawal_quantity

                                response.append(
                                    {
                                        "sector": sector.name,
                                        "product_code": product.code,
                                        "product_name": product.name,
                                        "entry_quantity": entry_quantity,
                                        "withdrawal_quantity": withdrawal_quantity,
                                        "entry_price": entry_price,
                                        "withdrawal_price": withdrawal_price,
                                    }
                                )
                else:
                    if public_defense_ids:
                        for public_defense_id in public_defense_ids:
                            public_defense = PublicDefense.objects.get(
                                id=public_defense_id
                            )
                            entry_filters = Q(
                                entry_date__gte=initial_date, entry_date__lte=final_date
                            )
                            entry_filters &= Q(stock_item__product_id=product_id)
                            entry_filters &= Q(
                                stock_item__stock__sector__public_defense_id=public_defense_id
                            )
                            entry_filters &= ~Q(stock_item__stock_id=1)
                            entry_quantity = (
                                StockEntry.objects.filter(entry_filters).aggregate(
                                    Sum("entry_quantity")
                                )["entry_quantity__sum"]
                                or 0
                            )
                            entry_price = product.price * entry_quantity

                            withdraw_filters = Q(
                                withdraw_date__gte=initial_date,
                                withdraw_date__lte=final_date,
                            )
                            withdraw_filters &= Q(stock_item__product_id=product_id)
                            withdraw_filters &= Q(
                                stock_item__stock__sector__public_defense_id=public_defense_id
                            )
                            withdraw_filters &= ~Q(stock_item__stock_id=1)
                            withdrawal_quantity = (
                                StockWithdrawal.objects.filter(
                                    withdraw_filters
                                ).aggregate(Sum("withdraw_quantity"))[
                                    "withdraw_quantity__sum"
                                ]
                                or 0
                            )
                            withdrawal_price = product.price * withdrawal_quantity

                            response.append(
                                {
                                    "public_defense": public_defense.name,
                                    "product_code": product.code,
                                    "product_name": product.name,
                                    "entry_quantity": entry_quantity,
                                    "withdrawal_quantity": withdrawal_quantity,
                                    "entry_price": entry_price,
                                    "withdrawal_price": withdrawal_price,
                                }
                            )
                    else:
                        for sector_id in sector_ids:
                            sector = Sector.objects.get(id=sector_id)
                            entry_filters = Q(
                                entry_date__gte=initial_date, entry_date__lte=final_date
                            )
                            entry_filters &= Q(stock_item__product_id=product_id)
                            entry_filters &= Q(stock_item__stock__sector_id=sector_id)
                            entry_filters &= ~Q(stock_item__stock_id=1)
                            entry_quantity = (
                                StockEntry.objects.filter(entry_filters).aggregate(
                                    Sum("entry_quantity")
                                )["entry_quantity__sum"]
                                or 0
                            )
                            entry_price = product.price * entry_quantity

                            withdraw_filters = Q(
                                withdraw_date__gte=initial_date,
                                withdraw_date__lte=final_date,
                            )
                            withdraw_filters &= Q(stock_item__product_id=product_id)
                            withdraw_filters &= Q(
                                stock_item__stock__sector_id=sector_id
                            )
                            withdraw_filters &= ~Q(stock_item__stock_id=1)
                            withdrawal_quantity = (
                                StockWithdrawal.objects.filter(
                                    withdraw_filters
                                ).aggregate(Sum("withdraw_quantity"))[
                                    "withdraw_quantity__sum"
                                ]
                                or 0
                            )
                            withdrawal_price = product.price * withdrawal_quantity

                            response.append(
                                {
                                    "sector": sector.name,
                                    "product_code": product.code,
                                    "product_name": product.name,
                                    "entry_quantity": entry_quantity,
                                    "withdrawal_quantity": withdrawal_quantity,
                                    "entry_price": entry_price,
                                    "withdrawal_price": withdrawal_price,
                                }
                            )
        else:
            product_ids = Product.objects.values_list("id", flat=True)
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                if categories:
                    if str(product.category_id) in categories:
                        if public_defense_ids:
                            for public_defense_id in public_defense_ids:
                                public_defense = PublicDefense.objects.get(
                                    id=public_defense_id
                                )
                                entry_filters = Q(
                                    entry_date__gte=initial_date,
                                    entry_date__lte=final_date,
                                )
                                entry_filters &= Q(stock_item__product_id=product_id)
                                entry_filters &= Q(
                                    stock_item__stock__sector__public_defense_id=public_defense_id
                                )
                                entry_filters &= ~Q(stock_item__stock_id=1)
                                entry_quantity = (
                                    StockEntry.objects.filter(entry_filters).aggregate(
                                        Sum("entry_quantity")
                                    )["entry_quantity__sum"]
                                    or 0
                                )
                                entry_price = product.price * entry_quantity

                                withdraw_filters = Q(
                                    withdraw_date__gte=initial_date,
                                    withdraw_date__lte=final_date,
                                )
                                withdraw_filters &= Q(stock_item__product_id=product_id)
                                withdraw_filters &= Q(
                                    stock_item__stock__sector__public_defense_id=public_defense_id
                                )
                                withdraw_filters &= ~Q(stock_item__stock_id=1)
                                withdrawal_quantity = (
                                    StockWithdrawal.objects.filter(
                                        withdraw_filters
                                    ).aggregate(Sum("withdraw_quantity"))[
                                        "withdraw_quantity__sum"
                                    ]
                                    or 0
                                )
                                withdrawal_price = product.price * withdrawal_quantity

                                response.append(
                                    {
                                        "public_defense": public_defense.name,
                                        "product_code": product.code,
                                        "product_name": product.name,
                                        "entry_quantity": entry_quantity,
                                        "withdrawal_quantity": withdrawal_quantity,
                                        "entry_price": entry_price,
                                        "withdrawal_price": withdrawal_price,
                                    }
                                )
                        else:
                            for sector_id in sector_ids:
                                sector = Sector.objects.get(id=sector_id)
                                entry_filters = Q(
                                    entry_date__gte=initial_date,
                                    entry_date__lte=final_date,
                                )
                                entry_filters &= Q(stock_item__product_id=product_id)
                                entry_filters &= Q(
                                    stock_item__stock__sector_id=sector_id
                                )
                                entry_filters &= ~Q(stock_item__stock_id=1)
                                entry_quantity = (
                                    StockEntry.objects.filter(entry_filters).aggregate(
                                        Sum("entry_quantity")
                                    )["entry_quantity__sum"]
                                    or 0
                                )
                                entry_price = product.price * entry_quantity

                                withdraw_filters = Q(
                                    withdraw_date__gte=initial_date,
                                    withdraw_date__lte=final_date,
                                )
                                withdraw_filters &= Q(stock_item__product_id=product_id)
                                withdraw_filters &= Q(
                                    stock_item__stock__sector_id=sector_id
                                )
                                withdraw_filters &= ~Q(stock_item__stock_id=1)
                                withdrawal_quantity = (
                                    StockWithdrawal.objects.filter(
                                        withdraw_filters
                                    ).aggregate(Sum("withdraw_quantity"))[
                                        "withdraw_quantity__sum"
                                    ]
                                    or 0
                                )
                                withdrawal_price = product.price * withdrawal_quantity

                                response.append(
                                    {
                                        "sector": sector.name,
                                        "product_code": product.code,
                                        "product_name": product.name,
                                        "entry_quantity": entry_quantity,
                                        "withdrawal_quantity": withdrawal_quantity,
                                        "entry_price": entry_price,
                                        "withdrawal_price": withdrawal_price,
                                    }
                                )
                else:
                    if public_defense_ids:
                        for public_defense_id in public_defense_ids:
                            public_defense = PublicDefense.objects.get(
                                id=public_defense_id
                            )
                            entry_filters = Q(
                                entry_date__gte=initial_date, entry_date__lte=final_date
                            )
                            entry_filters &= Q(stock_item__product_id=product_id)
                            entry_filters &= Q(
                                stock_item__stock__sector__public_defense_id=public_defense_id
                            )
                            entry_filters &= ~Q(stock_item__stock_id=1)
                            entry_quantity = (
                                StockEntry.objects.filter(entry_filters).aggregate(
                                    Sum("entry_quantity")
                                )["entry_quantity__sum"]
                                or 0
                            )
                            entry_price = product.price * entry_quantity

                            withdraw_filters = Q(
                                withdraw_date__gte=initial_date,
                                withdraw_date__lte=final_date,
                            )
                            withdraw_filters &= Q(stock_item__product_id=product_id)
                            withdraw_filters &= Q(
                                stock_item__stock__sector__public_defense_id=public_defense_id
                            )
                            withdraw_filters &= ~Q(stock_item__stock_id=1)
                            withdrawal_quantity = (
                                StockWithdrawal.objects.filter(
                                    withdraw_filters
                                ).aggregate(Sum("withdraw_quantity"))[
                                    "withdraw_quantity__sum"
                                ]
                                or 0
                            )
                            withdrawal_price = product.price * withdrawal_quantity

                            response.append(
                                {
                                    "public_defense": public_defense.name,
                                    "product_code": product.code,
                                    "product_name": product.name,
                                    "entry_quantity": entry_quantity,
                                    "withdrawal_quantity": withdrawal_quantity,
                                    "entry_price": entry_price,
                                    "withdrawal_price": withdrawal_price,
                                }
                            )
                    else:
                        for sector_id in sector_ids:
                            sector = Sector.objects.get(id=sector_id)
                            entry_filters = Q(
                                entry_date__gte=initial_date, entry_date__lte=final_date
                            )
                            entry_filters &= Q(stock_item__product_id=product_id)
                            entry_filters &= Q(stock_item__stock__sector_id=sector_id)
                            entry_filters &= ~Q(stock_item__stock_id=1)
                            entry_quantity = (
                                StockEntry.objects.filter(entry_filters).aggregate(
                                    Sum("entry_quantity")
                                )["entry_quantity__sum"]
                                or 0
                            )
                            entry_price = product.price * entry_quantity

                            withdraw_filters = Q(
                                withdraw_date__gte=initial_date,
                                withdraw_date__lte=final_date,
                            )
                            withdraw_filters &= Q(stock_item__product_id=product_id)
                            withdraw_filters &= Q(
                                stock_item__stock__sector_id=sector_id
                            )
                            withdraw_filters &= ~Q(stock_item__stock_id=1)
                            withdrawal_quantity = (
                                StockWithdrawal.objects.filter(
                                    withdraw_filters
                                ).aggregate(Sum("withdraw_quantity"))[
                                    "withdraw_quantity__sum"
                                ]
                                or 0
                            )
                            withdrawal_price = product.price * withdrawal_quantity

                            response.append(
                                {
                                    "sector": sector.name,
                                    "product_code": product.code,
                                    "product_name": product.name,
                                    "entry_quantity": entry_quantity,
                                    "withdrawal_quantity": withdrawal_quantity,
                                    "entry_price": entry_price,
                                    "withdrawal_price": withdrawal_price,
                                }
                            )

        if public_defense_ids:
            output_dict = {}
            for item in response:
                key = (item["product_code"], item["public_defense"])
                if key not in output_dict:
                    output_dict[key] = item
                else:
                    output_dict[key]["entry_quantity"] += item["entry_quantity"]
                    output_dict[key]["withdrawal_quantity"] += item[
                        "withdrawal_quantity"
                    ]
                    output_dict[key]["entry_price"] += item["entry_price"]
                    output_dict[key]["withdrawal_price"] += item["withdrawal_price"]

            response = list(output_dict.values())
        else:
            output_dict = {}
            for item in response:
                key = (item["product_code"], item["sector"])
                if key not in output_dict:
                    output_dict[key] = item
                else:
                    output_dict[key]["entry_quantity"] += item["entry_quantity"]
                    output_dict[key]["withdrawal_quantity"] += item[
                        "withdrawal_quantity"
                    ]
                    output_dict[key]["entry_price"] += item["entry_price"]
                    output_dict[key]["withdrawal_price"] += item["withdrawal_price"]

            response = list(output_dict.values())
        return Response(response)


class WarehouseItems(APIView):
    def get(self, request):
        queryset = (
            StockItem.objects.filter(stock__id=1)
            .select_related("product__measure")
            .values("product__code", "product__measure__name")
            .annotate(
                total_price=Cast(
                    Sum(
                        F("quantity") * F("product__price"),
                        filter=Q(product__code=F("product__code")),
                    ),
                    output_field=FloatField(),
                ),
                total_quantity=Sum(
                    "quantity", filter=Q(product__code=F("product__code"))
                ),
            )
            .order_by("product__code")
        )

        response_data = []
        for item in queryset:
            price = round(item["total_price"], 2)
            quantity = item["total_quantity"]
            average_price = round(price / quantity, 2) if quantity > 0 else 0
            code = item["product__code"]
            product = Product.objects.filter(code=code).first()
            item_data = {
                "product_name": product.name,
                "product_code": code,
                "product_measure": item["product__measure__name"],
                "price": price,
                "average_price": average_price,
                "quantity": quantity,
            }
            response_data.append(item_data)

        return Response(response_data)


class EmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data["subject"]
        message = serializer.validated_data["message"]
        recipients = Client.objects.values_list("email", flat=True)
        from_email = os.environ.get("EMAIL_HOST_USER")
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipients,
            reply_to=[from_email],
        )
        email.send()
        return Response({"message": "Email sent successfully"})
