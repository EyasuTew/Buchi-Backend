from bson import ObjectId
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_adoption():
    new_customer_response = client.post(
        'api/v1/customers', json={'name': 'FastAPI', 'phone_number': '1234'})
    assert new_customer_response.status_code == 200

    #CRETAE PET
    with open('app/tests/Cat.jpg', 'rb') as img:
        content = img.read()

    new_pet_response = client.post('api/v1/pets',
                           data={
                               "name": "PetName",
                               "pet_type": "dog",
                               "age": "baby",
                               "gender": "male",
                               "size": "small",
                               "good_with_children": True,
                           },
                           files=[
                               ('photos', ('buchi.jpg', content))
                           ],)

    assert new_pet_response.status_code == 200
    assert new_pet_response.json()['status'] == 'success'

    #VERIFY ADOPTION
    response = client.post('api/v1/adoptions',
                           json={
                               'customer_id': str(new_customer_response.json()["customerId"]),
                               'pet_id': str(new_pet_response.json()["petId"])
                           })

    assert response.status_code == 200
