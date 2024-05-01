import pytest
import sys
from unittest.mock import patch, MagicMock
sys.path.append('../web_app')
from flask import url_for

import api_server as api

@pytest.fixture
def client():
    with api.app.test_client() as client:
        yield client