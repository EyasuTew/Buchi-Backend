from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pets_list():
    response = client.get('api/v1/pets', params={'limit': 2})
    assert response.status_code == 200


def test_pets_post():

    dog_image_1 = None
    dog_image_2 = None
    with open('tests/test_files/dog-1.jpg', 'rb') as img:
        dog_image_1 = img.read()

    with open('tests/test_files/dog-2.jpg', 'rb') as img:
        dog_image_2 = img.read()

    response = client.post('api/v1/pets',
                           data={
                               "name": "Golden retriever dog",
                               "pet_type": "dog",
                               "age": "baby",
                               "gender": " male",
                               "size": "small",
                               "good_with_children": True,
                           },
                           files=[
                               ('photos', ('dog-1.jpg', dog_image_1)),
                               ('photos', ('dog-2.jpg', dog_image_2))

                           ],)

    assert response.status_code == 200
    assert response.json()['status'] == 'success'