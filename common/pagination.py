from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    def __init__(self):
        self.page_size_query_param = 'per_page'
        self.max_page_size = 100

    def get_paginated_response(self, data):
        return Response(data)
