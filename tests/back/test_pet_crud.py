import os
import time
import pytest
import requests
import allure
import json
from models.pets import Pet, Category, Tag
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL_BACK")
HEADERS = {"Content-Type": "application/json"}


def create_pet(pet: Pet):
    return requests.post(
        f"{BASE_URL}/pet",
        headers=HEADERS,
        data=json.dumps(pet, default=lambda o: o.__dict__)
    )


def find_pet_by_id(pet_id: int):
    return requests.get(f"{BASE_URL}/pet/{pet_id}", headers=HEADERS)


def update_pet(pet: Pet):
    return requests.put(
        f"{BASE_URL}/pet",
        headers=HEADERS,
        data=json.dumps(pet, default=lambda o: o.__dict__)
    )


def delete_pet(pet_id: int):
    return requests.delete(f"{BASE_URL}/pet/{pet_id}", headers=HEADERS)


@pytest.fixture
def new_pet():
    pet = Pet(
        id=int(time.time()),
        category=Category(id=1, name="Dogs"),
        name="Rex",
        photoUrls=["https://example.com/photo1.jpg"],
        tags=[Tag(id=1, name="Friendly")],
        status="available"
    )
    create_response = create_pet(pet)
    assert create_response.status_code == 200
    yield pet
    delete_pet(pet.id)


@allure.title("Create a new pet in the Petstore")
@allure.feature("Pet Management")
@allure.story("Create Pet")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_pet():
    pet = Pet(
        id=int(time.time()),
        category=Category(id=2, name="Cats"),
        name="Kitty",
        photoUrls=["https://example.com/cat.jpg"],
        tags=[Tag(id=2, name="Cute")],
        status="available"
    )
    response = create_pet(pet)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == pet.name
    assert data["status"] == pet.status

    delete_pet(pet.id)


@allure.title("Get a pet by ID from the Petstore")
@allure.feature("Pet Management")
@allure.story("Read Pet")
@allure.severity(allure.severity_level.NORMAL)
def test_get_pet_by_id(new_pet):
    max_attempts = 3
    for attempt in range(max_attempts):
        response = find_pet_by_id(new_pet.id)
        if response.status_code == 200:
            data = response.json()
            assert data["id"] == new_pet.id
            assert data["name"] == new_pet.name
            break
        time.sleep(2)
    else:
        pytest.fail(f"Pet with id {new_pet.id} was not found after {max_attempts} attempts")


@allure.title("Update an existing pet in the Petstore")
@allure.feature("Pet Management")
@allure.story("Update Pet")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_pet(new_pet):
    new_pet.name = "Max"
    new_pet.status = "sold"
    response = update_pet(new_pet)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Max"
    assert updated["status"] == "sold"


@allure.title("Delete a pet from the Petstore")
@allure.feature("Pet Management")
@allure.story("Delete Pet")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_pet(new_pet):
    delete_response = delete_pet(new_pet.id)
    assert delete_response.status_code == 200

    time.sleep(2)

    check = find_pet_by_id(new_pet.id)
    assert check.status_code == 404
