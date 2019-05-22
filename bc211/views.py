# The version is defined in /pathways-backend/bc211/__init__.py

from django.http import HttpResponse
from django.views.generic.base import View


class Bc211VersionView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(get_version_string())


def get_version_string():
    return __import__('bc211').__bc211_version__


def get_version_info():
    return __import__('bc211').__bc211_version_info__
