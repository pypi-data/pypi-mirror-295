"""
Fixtures for tests of :mod:`django_kanboard` application.

:creationdate: 06/07/2021 14:28
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.fixtures
"""
from datetime import timedelta
from typing import Any

import dotenv
import kanboard
import pytest
from django.utils.datetime_safe import datetime
from django.utils.timezone import get_current_timezone

CONFIG = dotenv.dotenv_values()

PROJECT_IDS = [
    122,
]

USERS_LIST: list[dict[str, Any]] = [
    {"user_id": 1, "kb_user_id": 12},
]

PROJECTS_LIST: list[dict[str, Any]] = [
    {
        "name": "Project 1",
        "owner_id": 12,
    },
    {
        "name": "Project 2",
        "owner_id": 12,
        "identifier": "PROJECT2",
    },
    {
        "name": "Project 3",
        "owner_id": 12,
        "identifier": "PROJECT3",
        "description": "Project 3 description",
    },
    {
        "name": "Project 4",
        "owner_id": 12,
        "identifier": "PROJECT4",
        "description": "Project 4 description",
        "start_date": datetime.now(get_current_timezone()),
    },
    {
        "name": "Project 5",
        "owner_id": 12,
        "identifier": "PROJECT5",
        "description": "Project 5 description",
        "start_date": datetime.now(get_current_timezone()) + timedelta(days=1),
        "end_date": datetime.now(get_current_timezone()) + timedelta(days=30),
    },
]


@pytest.fixture(scope="module")
def base_url() -> str:
    """
    Get the base_url for kanboard application.

    .. note:: Fixture !

    :return: URL
    """
    return CONFIG.get("base_url")


@pytest.fixture(scope="module")
def username() -> str:
    """
    Get the username for kanboard application.

    .. note:: Fixture !

    :return: username
    """
    return CONFIG.get("username")


@pytest.fixture(scope="module")
def token() -> str:
    """
    Get the token for kanboard application.

    .. note:: Fixture !

    :return: token
    """
    return CONFIG.get("token")


@pytest.fixture(scope="module")
def client() -> kanboard.Client:
    """
    Get a connected client application.

    .. note:: Fixture !

    :return: client
    """
    return kanboard.Client(
        url=CONFIG.get("base_url"),
        username=CONFIG.get("username"),
        password=CONFIG.get("token"),
    )


@pytest.fixture(scope="module")
def template_prefix() -> str:
    """
    Get the template_prefix used for syncing projects templates.

    .. note:: Fixture !

    :return: token
    """
    return CONFIG.get("template_prefix").strip('"')


@pytest.fixture(scope="module", params=USERS_LIST)
def user_mapping(request) -> dict[str, Any]:
    """
    Get user mappings between django user and kanboard user.

    .. note:: Fixture!

    :param request: Test request
    :return: Dict
    """
    return request.param


@pytest.fixture(scope="module", params=PROJECT_IDS)
def from_project_id(request) -> int:
    """
    Get a kanboard project id.

    .. note:: Fixture!

    :param request: Test request
    :return: Project id
    """
    return request.param


@pytest.fixture(scope="module", params=PROJECTS_LIST)
def project(request) -> dict[str, Any]:
    """
    Get a kanboard project data dict.

    .. note:: Fixture!

    :param request: Test request
    :return: Project data
    """
    return request.param


@pytest.fixture(scope="module")
def project_template_data() -> dict[str, Any]:
    """
    Get a kanboard template project data dict.

    .. note:: Fixture!

    :return: Template project data
    """
    return {
        "name": "Modèle : Test",
        "description": "",
        "id": 122,
    }


@pytest.fixture(scope="module")
def project_data() -> dict[str, Any]:
    """Get project data."""
    return {
        "title": "Project to copy",
        "description": "Project to copy",
    }
