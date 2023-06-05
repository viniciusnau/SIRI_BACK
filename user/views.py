import json
import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderMeSerializer
from stock.models import Category, StockItem
from stock.serializers import CategorySerializer, StockItemMeSerializer
from stock.services import get_stock_item_quantity

from .models import Client
from .serializers import ClientSerializer


class ClientListCreateView(generics.ListCreateAPIView):
    set = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]


class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]


class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        client = self.request.user.client
        stock = client.stock
        stock_items = StockItem.objects.filter(stock=stock).order_by("-created")
        filtered_stock_items_list = []

        for stock_item in stock_items:
            if stock_item.stock.id != 1:
                stock_item.quantity = get_stock_item_quantity(stock_item.id)
                stock_item.save(update_fields=["quantity"])
                if stock_item.quantity:
                    serializer = StockItemMeSerializer(stock_item)
                    filtered_stock_items_list.append(serializer.data)
            else:
                if stock_item.quantity:
                    serializer = StockItemMeSerializer(stock_item)
                    filtered_stock_items_list.append(serializer.data)

        filtered_stock_items_queryset = StockItem.objects.filter(
            pk__in=[item["id"] for item in filtered_stock_items_list]
        )

        orders_queryset = Order.objects.filter(client=client)

        categories = Category.objects.filter(sector=stock.sector)
        categories_serializer = CategorySerializer(categories, many=True)

        client_serializer = self.serializer_class(client)

        data = {
            "is_admin": self.request.user.is_superuser,
            "client": client_serializer.data,
            "categories": categories_serializer.data,
        }

        filtered_stock_items_page = self.paginate_queryset(
            filtered_stock_items_queryset
        )
        if filtered_stock_items_page is not None:
            filtered_stock_items_serializer = StockItemMeSerializer(
                filtered_stock_items_page, many=True
            )
            data["stock_items"] = filtered_stock_items_serializer.data
            data["stock_items_has_next"] = (
                len(filtered_stock_items_page) == self.paginator.page_size
            )
        else:
            filtered_stock_items_serializer = StockItemMeSerializer(
                filtered_stock_items_queryset, many=True
            )
            data["stock_items"] = filtered_stock_items_serializer.data
            data["stock_items_has_next"] = False
        if data["stock_items_has_next"]:
            data["next_stock_items"] = f"/stock/stock-items/?page=2&stock_id={stock.id}"
        else:
            data["next_stock_items"] = ""

        orders_page = self.paginate_queryset(orders_queryset)
        if orders_page is not None:
            orders_serializer = OrderMeSerializer(orders_page, many=True)
            data["orders"] = orders_serializer.data
            data["orders_has_next"] = len(orders_page) == self.paginator.page_size
        else:
            orders_serializer = OrderMeSerializer(orders_queryset, many=True)
            data["orders"] = orders_serializer.data
            data["orders_has_next"] = False
        if data["orders_has_next"]:
            data["next_orders"] = f"/order/?page=2&client_id={client.id}"
        else:
            data["next_orders"] = ""

        return Response(data)


@csrf_exempt
def password_reset(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        if email:
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            user.password_reset_token = token
            user.save()

            protocol = "https" if request.is_secure() else "http"
            domain = request.META["HTTP_HOST"]
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse(
                "user:confirm_password_reset",
                kwargs={
                    "uidb64": uidb64,
                    "token": token,
                },
            )

            context = {
                "user": user,
                "protocol": protocol,
                "domain": domain,
                "reset_url": reset_url,
            }
            email_html = render_to_string("password_reset.html", context)
            email_text = strip_tags(email_html)

            subject = "Resetar Senha"
            from_email = os.environ.get("EMAIL_HOST_USER")
            recipient_list = [email]

            email = EmailMultiAlternatives(
                subject=subject,
                body=email_text,
                from_email=from_email,
                to=recipient_list,
                reply_to=[from_email],
            )

            email.attach_alternative(email_html, "text/html")
            email.send()

            return JsonResponse({"message": "Password reset email sent."})

    return JsonResponse({"message": "Invalid request."}, status=400)


@csrf_exempt
def confirm_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                user.set_password(password)
                user.password_reset_token = None
                user.save()
                login(request, user)
                messages.success(request, "Sua senha foi redefinida com sucesso.")
                return render(
                    request,
                    "success.html",
                    {"message": "Sua senha foi redefinida com sucesso."},
                )
            else:
                messages.error(request, "As senhas não coincidem.")
                return render(
                    request, "error.html", {"message": "As senhas não coincidem."}
                )
        return render(request, "confirm_reset_password.html", {"valid_link": True})
    else:
        return render(
            request,
            "error.html",
            {"message": "O link de redefinição de senha é inválido."},
        )
