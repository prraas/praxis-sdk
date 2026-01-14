# tests/test_client.py
import os
import pytest
from praxis import Client


def test_client_requires_api_key():
    if "PRAXIS_API_KEY" in os.environ:
        del os.environ["PRAXIS_API_KEY"]

    with pytest.raises(ValueError):
        Client()


def test_client_initializes_with_key():
    client = Client(api_key="praxis-demo-key", base_url="https://api.prraas.tech")
    assert client.physics is not None
    assert client.navigation is not None
    assert client.simulation is not None
