from django.conf.urls import url, include
from django.contrib import admin

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^v1/forms/polls/', include('polls.web.urls')),
    url(r'^v1/', include('polls.web.api')),
    url(r'^v1/admin/', admin.site.urls),
]