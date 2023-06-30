from rest_framework.exceptions import APIException


class SupplierCannotBeDestroyedException(APIException):
    status_code = 400
    default_detail = (
        "This supplier cannot be deleted"
    )
    default_code = 5
