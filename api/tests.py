import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Dog, Breed
from .serializers import DogSerializer, BreedSerializer

client = APIClient()


class TestGetDogs(TestCase):
    """ Tests data acquisition for one/all dogs"""

    def setup(self):
        self.breed1 = Breed.objects.create(
            title="Labrador Retriever", description="Usual"
        )
        self.dog1 = Dog.objects.create(
            name="Jack",
            sex="MALE",
            coat_color="brown",
            behavior="CALM",
            breed=self.breed1,
            age=1,
        )
        self.dog2 = Dog.objects.create(
            name="Jessy",
            sex="FEMALE",
            coat_color="black",
            behavior="AGGRESSIVE",
            breed=self.breed1,
            age=2,
        )

    def test_get_dogs(self):
        """Tests receiving all dogs records"""
        response = client.get("/api/v1/dogs/")
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_one_dog(self):
        """
        Tests getting one dog by the correct link
        """
        response = client.get(f"/api/v1/dogs/{self.dog1.id}/")
        dog = Dog.objects.get(id=self.dog1.id)
        serializer = DogSerializer(dog)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_one_dog(self):
        """
        Tests getting one dog from the wrong link
        """
        response = client.get(f"/api/v1/dogs/{self.dog1.id + 10000}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_dogs(self):
        """
        Tests the search for dogs by name
        """
        response = client.get("/api/v1/dogs/?search=Jack")
        dog = Dog.objects.get(name="Jack")
        serializer = DogSerializer(dog)
        self.assertEqual(response.json(), [serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateDog(TestCase):
    """Test case for creating Dog record"""

    def setup(self):
        # Case with all fields filled
        self.valid_dog_1 = {
            "name": "Jack",
            "sex": "Male",
            "coat_color": "black",
            "behavior": "Aggressive",
            "breed": "Labrador Retriever",
            "age": 3,
        }
        # Case with the minimum number of filled fields
        self.valid_dog_2 = {
            "name": "Jack",
            "breed": "Labrador Retriever",
            "age": 5,
        }
        # Case with blank name
        self.invalid_dog = {
            "name": "",
            "sex": "Female",
            "coat_color": "pale",
            "behavior": "Calm",
            "breed": "Labrador Retriever",
        }

    def test_create_valid_dog(self):
        """Tests the creation of a dog record with correct data"""

        response_1 = client.post(
            "/api/v1/dogs/",
            data=json.dumps(self.valid_dog_1),
            content_type="application/json",
        )
        response_2 = client.post(
            "/api/v1/dogs/",
            data=json.dumps(self.valid_dog_2),
            content_type="application/json",
        )
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_dog(self):
        """Tests the creation of a dog record with incorrect data"""

        response = client.post(
            "/api/v1/dogs/",
            data=json.dumps(self.invalid_dog),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateDog(TestCase):
    """Tests updating dog data"""

    def setup(self):
        self.breed1 = Breed.objects.create(title="Лабрадор", description="Обычный")
        self.dog1 = Dog.objects.create(
            name="Jessy",
            sex="FEMALE",
            coat_color="brown",
            behavior="CALM",
            breed=self.breed1,
            age=9,
        )
        self.dog2 = Dog.objects.create(
            name="Bobby",
            sex="MALE",
            coat_color="black",
            behavior="AGGRESSIVE",
            breed=self.breed1,
            age=2,
        )
        # Case with filled name
        self.valid_dog = {
            "name": "Jessy",
            "sex": "Man",
            "coat_color": "black",
            "behavior": "Aggressive",
            "breed": "Sheepdog",
            "age": 5,
        }
        # Образец с незаполненным именем
        self.invalid_dog = {
            "name": "",
            "sex": "Female",
            "coat_color": "brown",
            "behavior": "Calm",
            "breed": "Labrador Retriever",
        }

    def test_valid_update_dog(self):
        """Tests updating dog data with correct data"""
        response = client.put(
            f"/api/v1/dogs/{self.dog1.id}/",
            data=json.dumps(self.valid_dog),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_dog(self):
        """Tests updating dog data with incorrect data"""
        response = client.put(
            f"/api/v1/dogs/{self.dog2.id}/",
            data=json.dumps(self.invalid_dog),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteDog(TestCase):
    """Tests the deletion of a dog object"""

    def setup(self):
        self.breed = Breed.objects.create(
            title="Golden Retriever", description="Simple"
        )
        self.dog1 = Dog.objects.create(
            name="Jane",
            sex="FEMALE",
            coat_color="brown",
            behavior="CALM",
            breed=self.breed,
            age=2,
        )

    def test_delete_dog(self):
        """Test case for deleting a dog object"""
        response = client.delete(f"/api/v1/dogs/{self.dog1.id}/")
        count = Dog.objects.all().count()
        self.assertEqual(0, count)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestGetBreed(TestCase):
    """Tests case for data acquisition of one / several breeds"""

    def setup(self):
        self.breed1 = Breed.objects.create(
            title="Labrador Retriever", description="Simple"
        )
        self.breed2 = Breed.objects.create(title="Outbred", description="Usual")

    def test_get_breeds(self):
        """Tests case for data acquisition of all breeds"""
        response = client.get("/api/v1/breeds/")
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_one_breed(self):
        """Tests the acquisition of data from one breed against the correct source data"""
        response = client.get(f"/api/v1/breeds/{self.breed1.id}/")
        breed = Breed.objects.get(id=self.breed1.id)
        serializer = BreedSerializer(breed)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_one_breed(self):
        """Tests fetching data from one dog against incorrect name"""
        response = client.get(f"/api/v1/breeds/{self.breed1.id + 1000}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCreateBreed(TestCase):
    """Testing the creation of a new breed"""

    def setup(self):
        self.valid_breed = {
            "title": "Akita",
            "description": "Akita Inu",
        }
        self.invalid_breed = {
            "title": "",
            "description": "Boxer Dog Breed",
        }

    def test_create_valid_breed(self):
        """Test case creation of a new breed with the correct data"""
        response = client.post(
            "/api/v1/breeds/",
            data=json.dumps(self.valid_breed),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_breed(self):
        """Tests the creation of a breed with the wrong name"""
        response = client.post(
            "/api/v1/breeds/",
            data=json.dumps(self.invalid_breed),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateBreed(TestCase):
    """Tests breed data update"""

    def setup(self):
        self.breed1 = Breed.objects.create(title="Barbet", description="Barbet Breed")
        self.breed2 = Breed.objects.create(
            title="Telomian", description="Telomian Breed"
        )
        self.valid_breed = {
            "title": "Barbet",
            "description": "Barbet Breed",
        }
        self.invalid_breed = {
            "title": "",
            "description": "Telomian Breed",
        }

    def test_valid_update_breed(self):
        """Tests updating breed data with correct data"""
        response = client.put(
            f"/api/v1/breeds/{self.breed1.id}/",
            data=json.dumps(self.valid_breed),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_breed(self):
        """Tests updating breed data with incorrect data"""
        response = client.put(
            f"/api/v1/breeds/{self.breed1.id}/",
            data=json.dumps(self.invalid_breed),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeteteBreed(TestCase):
    """Tests deleting breed"""

    def setup(self):
        self.breed = Breed.objects.create(
            title="English Water Spaniel", description="English Water Spaniel Breed"
        )

    def test_delete_breed(self):
        """Tests the removal breed data"""
        response = client.delete(f"/api/v1/breeds/{self.breed.id}/")
        count = Breed.objects.all().count()
        self.assertEqual(0, count)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
