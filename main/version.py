# The version is defined in /pathways-backend/main/__init__.py

from django.http import HttpResponse
from django.views.generic.base import View


class VersionView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(get_version_string())


def get_version_string():
    return __import__('main').__version__


def get_version_info():
    return __import__('main').__version_info__
