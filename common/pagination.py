from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    def __init__(self):
        self.page_query_param = 'page'
        self.page_size_query_param = 'per_page'
        self.max_page_size = 100

    def get_paginated_response(self, data):
        response = Response(data)
        headers = self.build_link_headers()
        if headers:
            response['Link'] = headers
        return response

    def build_link_headers(self):
        links = [('next', self.get_next_link()),
                 ('prev', self.get_previous_link())]

        headers = ['<{0}>; rel="{1}"'.format(url, name) for name, url in links if url]

        return ', '.join(headers) if headers else None
