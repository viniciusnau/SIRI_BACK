from django.urls import include, path

urlpatterns = [
    path("", include("user.urls")),
    path("stock/", include("stock.urls")),
    path("order/", include("order.urls")),
]
