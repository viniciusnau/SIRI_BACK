from rest_framework.exceptions import APIException


class SupplierCannotBeDestroyedException(APIException):
    status_code = 400
    default_detail = "This supplier cannot be deleted"
    default_code = 5


class ProtocolItemAlreadyExistsException(APIException):
    status_code = 400
    default_detail = "The requested protocol item already exists"
    default_code = 7
