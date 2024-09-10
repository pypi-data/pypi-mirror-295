"""
Tests the client connection.

:creationdate: 28/06/2021 14:28
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: tests.test_connection
"""
import kanboard  # noqa
import pytest  # noqa

from django_kanboard.kanboard_wrapper import KanboardWrapper
from .fixtures import *  # noqa


def test_connection(base_url, username, token):
    """
    Test the client connection.

    :param base_url: base server URL
    :param username: user_dict name
    :param token: API token or password
    :return: Nothing
    """
    kb = kanboard.Client(
        url=base_url,
        username=username,
        password=token,
    )
    assert kb


@pytest.mark.django_db
def test_client(base_url: str, username: str, token: str) -> None:
    """
    Test the client initialization.

    :param base_url: Kanboard application API URL
    :param username: Kanboard username
    :param token: Kanboard token
    :return: Nothing
    """
    _wrapper = KanboardWrapper(base_url=base_url, username=username, token=token)
    assert _wrapper.client
