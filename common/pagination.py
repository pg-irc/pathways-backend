from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

class Pagination(PageNumberPagination):
    def __init__(self):
        self.page_query_param = 'page'
        self.page_size_query_param = 'per_page'
        self.max_page_size = 100

    def get_paginated_response(self, data):
        response = Response(data)

        links = self.build_link_headers()
        if links:
            response['Link'] = links

        count = self.page.paginator.count
        if count:
            response['Count'] = count

        return response

    def build_link_headers(self):
        links = [('first', self.get_first_link()),
                 ('prev', self.get_previous_link()),
                 ('next', self.get_next_link()),
                 ('last', self.get_last_link())]

        headers = ['<{0}>; rel="{1}"'.format(url, name) for name, url in links if url]

        return ', '.join(headers) if headers else None

    def get_first_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.page_query_param)

    def get_last_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, self.page.paginator.num_pages)
