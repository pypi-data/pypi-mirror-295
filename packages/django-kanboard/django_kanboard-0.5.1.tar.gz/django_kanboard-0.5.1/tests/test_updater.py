"""
Test for :mod:`django_kanboard` application.

:creationdate: 01/07/2021 16:18
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.test_updater
"""
import logging
from typing import Any  # noqa

import pytest  # noqa
from django.contrib.auth import models as auth_models

from django_kanboard import models  # noqa
from django_kanboard.kanboard_wrapper import KanboardUpdater

from .fixtures import *  # noqa

logger = logging.getLogger(__name__)
__author__ = "fguerin"


@pytest.mark.django_db
def test_get_kanboard_user_id(base_url: str, username: str, token: str, user_mapping: dict[str, Any]) -> None:
    """
    Test the user grabbing.

    :param base_url: Kanboard application API URL
    :param username: Kanboard username
    :param token: Kanboard token
    :param user_mapping: User mapping
    :return: Nothing
    """
    _wrapper = KanboardUpdater(base_url=base_url, username=username, token=token)
    kb_user_id = _wrapper.get_kanboard_user_id(user_mapping["user_id"])
    assert kb_user_id == user_mapping["kb_user_id"]


@pytest.mark.django_db
def test_get_project_template(base_url: str, username: str, token: str, from_project_id: int) -> None:
    """
    Test the project grabbing.

    :param base_url: Kanboard application API URL
    :param username: Kanboard username
    :param token: Kanboard token
    :param from_project_id: Id of the project to copy
    :return: Nothing
    """
    _wrapper = KanboardUpdater(base_url=base_url, username=username, token=token)
    _project = _wrapper.get_project_dict(project_id=from_project_id)
    assert _project
    assert _project["tasks"]  # type: ignore
    for task in _project["tasks"]:  # type: ignore
        assert task["subtasks"]


@pytest.mark.django_db
def test_copy_project(base_url: str, username: str, token: str, from_project_id: int) -> None:
    """
    Test the copy of an existing kanboard project.

    :param base_url: Kanboard application API URL
    :param username: Kanboard username
    :param token: Kanboard token
    :param from_project_id: Id of the project to copy
    :return: Nothing
    """
    _wrapper = KanboardUpdater(base_url=base_url, username=username, token=token)
    project: dict[str, Any] = _wrapper.copy_project(
        from_project_id=from_project_id,
        user=auth_models.User.objects.get(pk=1),
        title="Copied project",
        description="Copied project",
    )
    assert project
    assert isinstance(project, dict)
    assert project["id"]
    assert project["name"] == "Copied project"
    assert project["description"] == "Copied project"


@pytest.mark.django_db
def test_create_project(base_url: str, username: str, token: str, project: dict[str, Any]) -> None:
    """Test the project creation."""
    _wrapper = KanboardUpdater(base_url=base_url, username=username, token=token)
    _project = _wrapper.create_project(**project)
    assert _project
