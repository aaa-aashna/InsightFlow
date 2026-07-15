import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.db.init_db import init_db
from main import app

init_db()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client
