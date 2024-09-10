"""
Models for :mod:`example_app` application.

:creationdate: 28/06/2021 15:54
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: example_app.models
"""
import logging

from django.db import models

logger = logging.getLogger(__name__)
__author__ = "fguerin"


class Project(models.Model):
    """Base project."""

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    kanboard_project = models.ForeignKey(
        "django_kanboard.Project",
        null=True,  # noqa
        blank=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        """Meta class."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        """
        Get the string representation for :class:`example_app.models.Project` instance.

        :return: Representation
        """
        return self.title
