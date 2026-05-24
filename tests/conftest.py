import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities

_original_activities = copy.deepcopy(app_activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(copy.deepcopy(_original_activities))
    yield


@pytest.fixture
def client():
    return TestClient(app)
