"""
Apps for :mod:`example` application.

:creationdate: 30/06/21 08:29
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: example.apps
"""
import logging

from django.contrib import admin

from example_app import models

logger = logging.getLogger(__name__)
__author__ = "fguerin"


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for :class:`example_app.models.Project` instances."""

    pass
