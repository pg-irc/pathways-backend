# The version is defined in /pathways-backend/bc211/__init__.py

from django.http import HttpResponse
from django.views.generic.base import View


class LastUpdateView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(get_last_update_string())


def get_last_update_string():
    return __import__('bc211').__last_update__


def get_last_update_info():
    return __import__('bc211').__last_update_info__
