import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b"Healthy" in response.data

def test_predict_endpoint(client):
    test_image = [[0] * 28 for _ in range(28)]
    response = client.post('/predict', json={"image": test_image})
    assert response.status_code == 200
    assert "prediction" in response.get_json()

def test_model_info_endpoint(client):
    response = client.get('/model/info')
    assert response.status_code == 200
    data = response.get_json()
    assert "model_name" in data
    assert "version" in data

def test_train_endpoint(client):
    payload = {
        "batch_size": 32,
        "epochs": 1,
        "optimizer": "adam"
    }
    response = client.post('/train', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert "message" in data
