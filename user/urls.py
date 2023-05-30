from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from swagger_config import schema_view
from .views import (
    ClientListCreateView,
    ClientRetrieveUpdateDestroyView,
    MeView,
    confirm_password_reset,
    password_reset,
)

app_name = "user"

urlpatterns = [
    path("login/", ObtainAuthToken.as_view(), name="login"),
    path("clients/", ClientListCreateView.as_view(), name="client_list_create"),
    path(
        "clients/<int:pk>/",
        ClientRetrieveUpdateDestroyView.as_view(),
        name="client_retrieve_update_destroy",
    ),
    path("me/", MeView.as_view(), name="me"),
    path("password-reset/", csrf_exempt(password_reset), name="password_reset"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        csrf_exempt(confirm_password_reset),
        name="confirm_password_reset",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
