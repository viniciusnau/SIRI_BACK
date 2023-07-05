from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class InfinitePagination(LimitOffsetPagination):
    default_limit = 100000000000
    max_limit = 100000000000


class SupplierOrderItemPagination(PageNumberPagination):
    page_size = 15
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
