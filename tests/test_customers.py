from fastapi.testclient import TestClient

from app.main import app
import random
client = TestClient(app)


def test_customers():
    phone_number = str(random.randint(11111111, 99999999))
    name = "TestCustomer-"+str(random.randint(11111111, 99999999))
    response = client.post(
        'api/v1/customers', json={'name': name, 'phone_number': phone_number})
    assert response.status_code == 200
