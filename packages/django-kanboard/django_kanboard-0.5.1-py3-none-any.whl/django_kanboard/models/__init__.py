"""
Models for :mod:`django_kanboard` application.

:creationdate: 28/06/2021 12:11
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: django_kanboard.models
"""
import logging
import pprint
from typing import Any

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.datetime_safe import date
from django.utils.translation import gettext as _
from django_currentuser.middleware import get_current_authenticated_user

from django_kanboard import kanboard_wrapper

from .config import KanboardConfig
from .helpers import Administrable

logger = logging.getLogger(__name__)
__author__ = "fguerin"


__all__ = [
    "KanboardConfig",
]


class Project(Administrable, models.Model):
    """Bound project."""

    # region Fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField(
        verbose_name=_("relative entity"),
    )

    content_object = GenericForeignKey()

    project_template = models.ForeignKey(
        "django_kanboard.ProjectTemplate",
        verbose_name=_("project template"),
        on_delete=models.CASCADE,
    )

    kanboard_project_id = models.PositiveIntegerField(
        verbose_name=_("kanboard project id"),
    )

    board_url = models.URLField(
        verbose_name=_("board URL"),
        blank=True,
    )

    calendar_url = models.URLField(
        verbose_name=_("calendar URL"),
        blank=True,
    )

    list_url = models.URLField(
        verbose_name=_("list URL"),
        blank=True,
    )
    # endregion Fields

    class Meta:
        """Meta class."""

        verbose_name = _("Bound project")
        verbose_name_plural = _("Bound projects")

    def __str__(self):
        """
        Get the str representation of the :class:`django_kanboard.models.Project` instance.

        :return: Content object
        """
        return self.content_object


class ProjectTemplate(Administrable, models.Model):
    """ProjectTemplate schema."""

    # region Fields
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )

    description = models.TextField(  # noqa
        verbose_name=_("description"),
        blank=True,
        null=True,
        default="",
    )

    kanboard_project_id = models.PositiveIntegerField(
        verbose_name=_("project template id"),
    )
    # endregion Fields

    class Meta:
        """Meta class."""

        verbose_name = _("Project template")
        verbose_name_plural = _("Project templates")

    def __str__(self):
        """
        Get the str representation of the :class:`django_kanboard.models.ProjectTemplate` instance.

        :return: Template name
        """
        return self.name

    def create_project(self, from_project: models.Model) -> Project:
        updater = kanboard_wrapper.KanboardUpdater()
        title = getattr(from_project, "title", None) or getattr(from_project, "name", None)
        description = getattr(from_project, "description", "")
        user = get_current_authenticated_user()

        params = {
            "title": title,
            "description": description,
            "user": user,
            "start_date": date.today(),
        }

        if hasattr(from_project, "due_at") and from_project.due_at:
            params.update({"end_date": from_project.due_at})

        new_project: dict[str, Any] = updater.copy_project(
            from_project_id=self.kanboard_project_id,
            **params,
        )
        logger.info(
            "%s::create_project() Kanboard project created: %s",
            self.__class__.__name__,
            pprint.pformat(new_project),
        )
        return Project.objects.create(
            content_type=ContentType.objects.get_for_model(from_project),
            object_id=from_project.pk,
            project_template=self,
            kanboard_project_id=new_project["id"],
            board_url=new_project["url"]["board"],
            list_url=new_project["url"]["list"],
            calendar_url=new_project["url"]["calendar"],
        )


class KanboardUser(models.Model):
    """Binding between Kanboard user and Django :class:`django:django.contrib.auth.models.User`."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="kanboard_user",
        on_delete=models.CASCADE,
    )

    kanboard_user_id = models.PositiveIntegerField(
        verbose_name=_("kanboard user id"),
    )

    class Meta:
        """Meta class."""

        verbose_name = _("Kanboard user")
        verbose_name_plural = _("Kanboard users")

    def __str__(self):
        """
        Get the str representation of the :class:`django_kanboard.models.KanboardUser` instance.

        :return: Kanboard user
        """
        return f"{self.user} ({self.kanboard_user_id})"


class KanboardGroup(models.Model):
    """Binding between Kanboard group and Django :class:`django:django.contrib.auth.models.Group`."""

    group = models.OneToOneField(
        "auth.Group",
        verbose_name=_("group"),
        related_name="kanboard_group",
        on_delete=models.CASCADE,
    )

    kanboard_group_id = models.PositiveIntegerField(
        verbose_name=_("kanboard group id"),
    )

    class Meta:
        """Meta class."""

        verbose_name = _("Kanboard group")
        verbose_name_plural = _("Kanboard groups")

    def __str__(self):
        """
        Get the str representation of the :class:`django_kanboard.models.KanboardGropp` instance.

        :return: Kanboard group
        """
        return f"{self.group} ({self.kanboard_group_id})"
