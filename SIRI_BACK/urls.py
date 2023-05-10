from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="SIRI",
        default_version='v1',
        description="SIRI is a Django-based project developed for DPESC, aimed at efficiently managing internal "
                    "processes within the organization.",
        terms_of_service="",
        contact=openapi.Contact(email="suporte-getig@defensoria.sc.gov.br"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", include("user.urls")),
    path("stock/", include("stock.urls")),
    path("order/", include("order.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
