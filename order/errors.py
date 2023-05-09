from rest_framework.exceptions import APIException


class OrderAlreadyAddedToStockException(APIException):
    status_code = 400
    default_detail = (
        "This order has already been partially or completely added to the stock"
    )
    default_code = 1


class RestrictedDateException(APIException):
    status_code = 451
    default_detail = "The system is not open today"
    default_code = 2


class MaterialsOrderAlreadyExistsException(
    APIException,
):
    status_code = 409
    default_detail = "The requested material order already exists"
    default_code = 3
