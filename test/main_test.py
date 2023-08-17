from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.join(os.path.abspath('..')))
#sys.path.append(os.path.join(os.path.abspath('../src")))
from src.utils.users import *
from src.utils.db import *
from src import connection

from src.connection import *
from src.main import app


client = TestClient(app)


# def test_root():
#    response = client.get("/api/healthchecker")
#    assert response.status_code == 200
#    assert response.json() == {"message": "Well connected to the API"}
