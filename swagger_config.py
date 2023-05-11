from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="SIRI",
        default_version="v1",
        description="SIRI is a Django-based project developed for DPESC, aimed at efficiently managing "
        "internal processes within the organization.",
        terms_of_service="",
        contact=openapi.Contact(email="suporte-getig@defensoria.sc.gov.br"),
        license=openapi.License(name=""),
    ),
    public=True,
)
