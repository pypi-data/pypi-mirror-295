"""
Apps for :mod:`example` application.

:creationdate: 30/06/21 08:29
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: example.apps
"""
from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    """Example app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "example_app"
