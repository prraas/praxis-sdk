# tests/test_client.py
import os
import pytest
from robostream import Client


def test_client_requires_api_key():
    if "ROBOSTREAM_API_KEY" in os.environ:
        del os.environ["ROBOSTREAM_API_KEY"]

    with pytest.raises(ValueError):
        Client()


def test_client_initializes_with_key():
    client = Client(api_key="robostream-demo-key")
    assert client.physics is not None
    assert client.navigation is not None
    assert client.simulation is not None
