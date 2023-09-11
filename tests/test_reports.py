from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_report():
    response = client.get("/api/v1/generateReport",
                          params={'fromDate': '2023-02-02', 'toDate': '2023-03-03'})

    assert response.status_code == 200