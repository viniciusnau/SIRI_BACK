from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 100000000000
    max_limit = 100000000000
