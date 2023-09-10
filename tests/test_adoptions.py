from bson import ObjectId
from fastapi.testclient import TestClient

from app.main import app
import random

client = TestClient(app)


def test_create_adoption():

    phone_number = str(random.randint(11111111, 99999999))
    name = "TestCustomer-" + str(random.randint(11111111, 99999999))
    new_customer_response = client.post(
        'api/v1/customers', json={'name': name, 'phone_number': phone_number})

    #CRETAE PET
    dog_image_1 = None
    dog_image_2 = None
    with open('tests/test_files/dog-1.jpg', 'rb') as img:
        dog_image_1 = img.read()

    with open('tests/test_files/dog-2.jpg', 'rb') as img:
        dog_image_2 = img.read()

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
                               ('photos', ('dog-1.jpg', dog_image_1)),
                               ('photos', ('dog-2.jpg', dog_image_2))
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
    print(response.json())
