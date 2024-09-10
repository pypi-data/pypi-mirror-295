"""
Tests the syncer class.

:creationdate: 28/06/2021 14:28
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.test_connection
"""
import logging

from django.contrib.auth import models as auth_models

from django_kanboard import models
from django_kanboard.kanboard_wrapper import KanboardSyncer

from .fixtures import *  # noqa

logger = logging.getLogger(__name__)


@pytest.mark.django_db  # noqa: F405
def test_template_syncer(
    base_url: str,
    username: str,
    token: str,
    template_prefix: str,
) -> None:
    """
    Test the template syncer.

    :param user_dict: Default user_dict, needed for project template creation
    :param base_url: base server URL
    :param username: user_dict name
    :param token: API token or password
    :return: Nothing
    """
    # start syncing templates...
    syncer = KanboardSyncer(
        base_url=base_url,
        username=username,
        token=token,
    )
    syncer.sync_templates(template_prefix=template_prefix)
    assert models.ProjectTemplate.objects.count()


@pytest.mark.django_db  # noqa: F405
def test_sync_users(
    base_url: str,
    username: str,
    token: str,
):
    """Test the user sync."""
    syncer = KanboardSyncer(
        base_url=base_url,
        username=username,
        token=token,
    )
    syncer.sync_users()
    for user in auth_models.User.objects.all():
        assert hasattr(user, "kanboard_user")


@pytest.mark.django_db  # noqa: F405
def test_sync_groups(
    base_url: str,
    username: str,
    token: str,
):
    """Test the groups sync."""
    syncer = KanboardSyncer(
        base_url=base_url,
        username=username,
        token=token,
    )
    syncer.sync_groups()
    for group in auth_models.Group.objects.all():
        assert hasattr(group, "kanboard_group")
