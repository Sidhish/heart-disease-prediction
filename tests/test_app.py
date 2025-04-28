import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Heart Disease Prediction" in response.data

def test_prediction_endpoint(client):
    test_data = {
        'age': '52',
        'sex': '1',
        'cp': '0',
        'trestbps': '125',
        'chol': '212',
        'fbs': '0',
        'restecg': '1',
        'thalach': '168',
        'exang': '0',
        'oldpeak': '1.0',
        'slope': '2',
        'ca': '2',
        'thal': '3'
    }
    response = client.post('/predict', data=test_data)
    assert response.status_code == 200
    assert b"Prediction Result:" in response.data