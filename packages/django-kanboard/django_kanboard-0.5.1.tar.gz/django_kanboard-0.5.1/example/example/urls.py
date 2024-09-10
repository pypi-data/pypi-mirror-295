"""
example URL Configuration.

:creationdate: 29/06/2021 16:48
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: example.urls
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]
