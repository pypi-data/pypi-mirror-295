"""
Test models for :mod:`django_kanboard` application.

:creationdate: 08/07/2021 09:52
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.test_models
"""
import logging
from typing import Any  # noqa

import pytest  # noqa
from example_app import models as example_models

from django_kanboard import models

from .fixtures import *  # noqa

logger = logging.getLogger(__name__)
__author__ = "fguerin"


@pytest.mark.django_db
def test_create_template(project_template_data: dict[str, Any], project_data: dict[str, Any]) -> None:
    """Test template creation."""
    # Create the template
    template = models.ProjectTemplate.objects.create(
        name=project_template_data["name"],
        description=project_template_data["description"],
        kanboard_project_id=project_template_data["id"],
    )

    # Create the project
    _project = example_models.Project.objects.create(
        title=project_data["title"],
        description=project_data["description"],
    )

    # Create from copy
    new_project = template.create_project(from_project=_project)
    assert isinstance(new_project, models.Project)
