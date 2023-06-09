import datetime
import os
import tempfile

import boto3
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from stock.models import (
    Category,
    DispatchReport,
    ProtocolItem,
    ReceivingReport,
    Stock,
    StockItem,
    Supplier,
)
from stock.pagination import SupplierOrderItemPagination
from user.models import Client

from .errors import (
    MaterialsOrderAlreadyExistsException,
    OrderAlreadyAddedToStockException,
    QuantityTooBigException,
    RestrictedDateException,
    SupplierOrderItemAlreadyExistsException,
)
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
from .serializers import (
    MaterialsOrderSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProtocolWithdrawalSerializer,
    RetrieveMaterialsOrderSerializer,
    RetrieveOrderItemSerializer,
    RetrieveOrderSerializer,
    RetrieveProtocolWithdrawalSerializer,
    RetrieveStockEntrySerializer,
    RetrieveStockWithdrawalSerializer,
    RetrieveSupplierOrderItemSerializer,
    RetrieveSupplierOrderSerializer,
    StockEntrySerializer,
    StockWithdrawalSerializer,
    SupplierOrderItemSerializer,
    SupplierOrderSerializer,
)

client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION_NAME"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = RetrieveOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        restricted_dates = os.environ.get("RESTRICTED_DATES").strip("][").split(",")
        today = datetime.date.today().strftime("%d/%m/%Y")
        if today in restricted_dates:
            raise RestrictedDateException()
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveOrderSerializer
        elif self.request.method in ["POST"]:
            return OrderSerializer


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = RetrieveOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        file_data = self.request.data.get("file")
        if file_data:
            with tempfile.TemporaryFile() as tmp_file:
                for chunk in file_data.file:
                    tmp_file.write(chunk)
                tmp_file.seek(0)
                client.upload_fileobj(
                    tmp_file,
                    os.environ.get("AWS_BUCKET_NAME"),
                    f"confirm-order/{instance.id}",
                )
            instance.file = str(instance.id)
        instance.save()

    def perform_destroy(self, instance):
        if instance.partially_added_to_stock or instance.completely_added_to_stock:
            raise OrderAlreadyAddedToStockException()
        instance.delete()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveOrderSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return OrderSerializer


class AllOrderItemsView(generics.GenericAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = RetrieveOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_ids = self.request.query_params.get("order_id")
        if order_ids:
            order_ids = order_ids.split(",")
            queryset = queryset.filter(order__id__in=order_ids)
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = RetrieveOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        order_ids = self.request.query_params.get("order_id")
        if order_ids:
            order_ids = order_ids.split(",")
            queryset = queryset.filter(order__id__in=order_ids)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data if isinstance(request.data, list) else [request.data]
        if self.request.user.client.stock.id == 1:
            for item in data:
                item["supplier_quantity"] = item["quantity"]
        serializer = OrderItemSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()


class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = RetrieveOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        description = self.request.query_params.get("description")
        if description:
            recipient = Client.objects.get(id=instance.order.client.id).email
            from_email = os.environ.get("EMAIL_HOST_USER")
            email = EmailMultiAlternatives(
                subject=f"Item {instance.product.name} do pedido {instance.order.id} NEGADO",
                body=f"Motivo: {description}",
                from_email=from_email,
                to=[recipient],
                reply_to=[from_email],
            )
            email.send()
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderItemSerializer(
            instance, data=request.data, partial=kwargs.get("partial", False)
        )
        serializer.is_valid(raise_exception=True)
        added_quantity = serializer.validated_data.get("added_quantity")
        warehouse_stock = Stock.objects.get(id=1)
        user_stock = request.user.client.stock

        if added_quantity and added_quantity > instance.quantity:
            raise QuantityTooBigException

        if instance.added_quantity == 0 and added_quantity:
            stock_item, created = StockItem.objects.get_or_create(
                product=instance.product, stock=user_stock
            )
            if user_stock.id == warehouse_stock.id:
                stock_item.quantity = stock_item.quantity + added_quantity
                stock_item.save(update_fields=["quantity"])
                ReceivingReport.objects.create(
                    supplier=instance.supplier,
                    product=instance.product,
                    quantity=instance.supplier_quantity,
                )
            if user_stock.id != warehouse_stock.id:
                stock_entry = StockEntry.objects.create(
                    order_item=instance,
                    stock_item=stock_item,
                    entry_quantity=added_quantity,
                )
                quantity = stock_entry.entry_quantity - instance.added_quantity
                if (
                    instance.supplier_quantity
                    and instance.quantity == added_quantity
                    and instance.supplier
                ):
                    warehouse_stock_item, created = StockItem.objects.get_or_create(
                        stock=warehouse_stock, product=instance.product
                    )
                    warehouse_stock_item.quantity = (
                        warehouse_stock_item.quantity + instance.supplier_quantity
                    )
                    warehouse_stock_item.save(update_fields=["quantity"])
                    ReceivingReport.objects.create(
                        supplier=instance.supplier,
                        product=instance.product,
                        quantity=instance.supplier_quantity,
                    )
                warehouse_stock_item = StockItem.objects.get(
                    stock=warehouse_stock, product=instance.product
                )
                warehouse_stock_item.quantity = warehouse_stock_item.quantity - quantity
                warehouse_stock_item.save(update_fields=["quantity"])
                DispatchReport.objects.create(
                    product=stock_item.product,
                    quantity=quantity,
                    public_defense=stock_entry.stock_item.stock.sector.public_defense,
                )
        elif instance.added_quantity != added_quantity and added_quantity:
            if user_stock.id == warehouse_stock.id:
                stock_item, created = StockItem.objects.get_or_create(
                    product=instance.product, stock=warehouse_stock
                )
                stock_item.quantity = stock_item.quantity + added_quantity
                stock_item.save(update_fields=["quantity"])
                ReceivingReport.objects.create(
                    supplier=instance.supplier,
                    product=instance.product,
                    quantity=instance.supplier_quantity,
                )
            if user_stock.id != warehouse_stock.id:
                stock_entry = StockEntry.objects.get(order_item=instance)
                stock_entry.entry_quantity = added_quantity
                stock_entry.save(update_fields=["entry_quantity"])
                stock_entry = StockEntry.objects.get(order_item=instance)
                quantity = stock_entry.entry_quantity - instance.added_quantity
                if (
                    instance.supplier_quantity
                    and instance.quantity == added_quantity
                    and instance.supplier
                ):
                    warehouse_stock_item = StockItem.objects.get(
                        stock=warehouse_stock, product=instance.product
                    )
                    warehouse_stock_item.quantity = (
                        warehouse_stock_item.quantity + instance.supplier_quantity
                    )
                    warehouse_stock_item.save(update_fields=["quantity"])
                    ReceivingReport.objects.create(
                        supplier=instance.supplier,
                        product=instance.product,
                        quantity=instance.supplier_quantity,
                    )
                warehouse_stock_item = StockItem.objects.get(
                    stock=warehouse_stock, product=instance.product
                )
                warehouse_stock_item.quantity = warehouse_stock_item.quantity - quantity
                warehouse_stock_item.save(update_fields=["quantity"])
                DispatchReport.objects.create(
                    product=stock_entry.stock_item.product,
                    quantity=quantity,
                    public_defense=stock_entry.stock_item.stock.sector.public_defense,
                )

        self.perform_update(serializer)

        order_items = OrderItem.objects.filter(order=instance.order)
        all_quantities_added = all(
            order_item.quantity == order_item.added_quantity
            for order_item in order_items
        )
        any_quantity_added = any(
            order_item.added_quantity != 0 for order_item in order_items
        )

        if all_quantities_added:
            instance.order.completely_added_to_stock = True
            instance.order.partially_added_to_stock = False
            instance.order.is_sent = True
        elif any_quantity_added:
            instance.order.partially_added_to_stock = True
            instance.order.completely_added_to_stock = False
            instance.order.is_sent = True

        instance.order.save(
            update_fields=[
                "completely_added_to_stock",
                "partially_added_to_stock",
                "is_sent",
            ]
        )

        return Response(serializer.data)


class StockWithdrawalListCreateView(generics.ListCreateAPIView):
    queryset = StockWithdrawal.objects.all()
    serializer_class = RetrieveStockWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_item_ids = self.request.query_params.get("stock_item_id")
        if stock_item_ids:
            stock_item_ids = stock_item_ids.split(",")
            queryset = queryset.filter(stock_item__id__in=stock_item_ids)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockWithdrawalSerializer
        elif self.request.method in ["POST"]:
            return StockWithdrawalSerializer


class StockWithdrawalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockWithdrawal.objects.all()
    serializer_class = RetrieveStockWithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockWithdrawalSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return StockWithdrawalSerializer


class StockEntryListCreateView(generics.ListCreateAPIView):
    queryset = StockEntry.objects.all()
    serializer_class = RetrieveStockEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_item_ids = self.request.query_params.get("stock_item_id")
        if stock_item_ids:
            stock_item_ids = stock_item_ids.split(",")
            queryset = queryset.filter(stock_item__id__in=stock_item_ids)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockEntrySerializer
        elif self.request.method in ["POST"]:
            return StockEntrySerializer


class StockEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockEntry.objects.all()
    serializer_class = RetrieveStockEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveStockEntrySerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return StockEntrySerializer


class SupplierOrderListCreateView(generics.ListCreateAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = RetrieveSupplierOrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier_ids = self.request.query_params.get("supplier_id")
        if supplier_ids:
            supplier_ids = supplier_ids.split(",")
            queryset = queryset.filter(supplier__id__in=supplier_ids)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSupplierOrderSerializer
        elif self.request.method in ["POST"]:
            return SupplierOrderSerializer


class SupplierOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupplierOrder.objects.all()
    serializer_class = RetrieveSupplierOrderSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSupplierOrderSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return SupplierOrderSerializer


class SupplierOrderItemListCreateView(generics.ListCreateAPIView):
    queryset = SupplierOrderItem.objects.all()
    serializer_class = RetrieveSupplierOrderItemSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            SupplierOrderItem.objects.get(
                product_id=request.data.get("product"),
                supplier_order_id=request.data.get("supplier_order"),
            )
            raise SupplierOrderItemAlreadyExistsException()
        except ObjectDoesNotExist:
            pass
        response = super().create(request, *args, **kwargs)
        supplier_order_item = self.queryset.get(id=response.data["id"])
        protocol = supplier_order_item.supplier_order.protocol
        protocol_item = ProtocolItem.objects.get(
            protocol=protocol, product=supplier_order_item.product
        )
        ProtocolWithdrawal.objects.create(
            withdraw_quantity=supplier_order_item.quantity,
            protocol_item=protocol_item,
            supplier_order_item=supplier_order_item,
        )
        return response

    def list(self, request, *args, **kwargs):
        supplier_id = self.request.query_params.get("supplier_id")
        initial_date = self.request.query_params.get("initial_date")
        final_date = self.request.query_params.get("final_date")
        category_id = self.request.query_params.get("category_id")

        if not (supplier_id and initial_date and final_date and category_id):
            self.pagination_class = SupplierOrderItemPagination
            queryset = super().get_queryset()
            supplier_order_ids = self.request.query_params.get("supplier_order_id")
            if supplier_order_ids:
                supplier_order_ids = supplier_order_ids.split(",")
                queryset = queryset.filter(supplier_order__id__in=supplier_order_ids)
            paginated_queryset = self.paginate_queryset(queryset)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            initial_date = parse_date(initial_date)
            final_date = parse_date(final_date)
            category = Category.objects.get(id=category_id)
        except (ValueError, Supplier.DoesNotExist, Category.DoesNotExist):
            return Response(
                {"detail": "Invalid query parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        supplier_orders = (
            SupplierOrder.objects.filter(
                supplier=supplier,
                created__date__gte=initial_date,
                created__date__lte=final_date,
                protocol__category=category,
            )
            .annotate(total_quantity=Sum("supplierorderitem__quantity"))
            .order_by("id")
        )

        supplier_orders_list = []
        for supplier_order in supplier_orders:
            supplier_order_items = supplier_order.supplierorderitem_set.all().order_by(
                "product__name"
            )
            supplier_order_items_list = []
            for supplier_order_item in supplier_order_items:
                supplier_order_items_list.append(
                    {
                        "product": supplier_order_item.product.name,
                        "code": supplier_order_item.product.code,
                        "quantity": supplier_order_item.quantity,
                    }
                )

            supplier_orders_list.append(
                {
                    "public_defense": supplier_order.public_defense.name,
                    "supplier_order_items": supplier_order_items_list,
                }
            )

        materials_order, created = MaterialsOrder.objects.get_or_create(
            supplier=supplier,
            category=category,
            date_range=str(initial_date) + " - " + str(final_date),
        )
        if not created:
            raise MaterialsOrderAlreadyExistsException()

        data = {
            "supplier": supplier.name,
            "category": category.name,
            "materials_order": materials_order.id,
            "supplier_orders": supplier_orders_list,
        }
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveSupplierOrderItemSerializer
        elif self.request.method in ["POST"]:
            return SupplierOrderItemSerializer


class SupplierOrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupplierOrderItem.objects.all()
    serializer_class = SupplierOrderItemSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        ProtocolWithdrawal.objects.get(supplier_order_item=instance).delete()
        instance.delete()


class ProtocolWithdrawalListCreateView(generics.ListCreateAPIView):
    queryset = ProtocolWithdrawal.objects.all()
    serializer_class = RetrieveProtocolWithdrawalSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveProtocolWithdrawalSerializer
        elif self.request.method in ["POST"]:
            return ProtocolWithdrawalSerializer


class ProtocolWithdrawalRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = ProtocolWithdrawal.objects.all()
    serializer_class = ProtocolWithdrawalSerializer
    permission_classes = [IsAdminUser]


class MaterialsOrderListCreateView(generics.ListCreateAPIView):
    queryset = MaterialsOrder.objects.all()
    serializer_class = RetrieveMaterialsOrderSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveMaterialsOrderSerializer
        elif self.request.method in ["POST"]:
            return MaterialsOrderSerializer


class MaterialsOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaterialsOrder.objects.all()
    serializer_class = RetrieveMaterialsOrderSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.save()
        file_data = self.request.data.get("file")
        client.upload_fileobj(
            file_data,
            os.environ.get("AWS_BUCKET_NAME"),
            f"materials-order/{instance.id}",
        )
        instance.file = str(instance.id)
        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RetrieveMaterialsOrderSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return MaterialsOrderSerializer
