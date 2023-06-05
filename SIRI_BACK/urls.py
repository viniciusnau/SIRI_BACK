from django.urls import include, path

from swagger_config import schema_view

urlpatterns = [
    path("", include("user.urls")),
    path("stock/", include("stock.urls")),
    path("order/", include("order.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
