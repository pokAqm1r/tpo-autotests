"""Автотесты API пользователей. Повторяют проверки из Postman-коллекции."""
import time

import pytest

# Ожидаемая структура пользователя: поле -> тип (вложенный dict = объект)
USER_SCHEMA = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    "address": {"street": str, "city": str, "zipcode": str,
                "geo": {"lat": str, "lng": str}},
    "phone": str,
    "company": {"name": str},
}


def assert_matches_schema(data, schema, path="user"):
    """Проверяет, что в data есть все поля схемы и у них нужные типы."""
    assert isinstance(data, dict), f"{path} должен быть объектом"
    for field, expected in schema.items():
        assert field in data, f"нет поля {path}.{field}"
        if isinstance(expected, dict):
            assert_matches_schema(data[field], expected, f"{path}.{field}")
        else:
            assert isinstance(data[field], expected), \
                f"{path}.{field} должно иметь тип {expected.__name__}"


# ---------- GET /users ----------

def test_get_users_list(api, base_url):
    response = api.get(f"{base_url}/users")

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 10
    for user in users:
        assert {"id", "name", "username", "email"} <= user.keys()
        assert "@" in user["email"]


# ---------- GET /users/{id} ----------

def test_get_user_status_and_response_time(api, base_url):
    response = api.get(f"{base_url}/users/1")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2


def test_get_user_json_structure(api, base_url):
    response = api.get(f"{base_url}/users/1")

    assert_matches_schema(response.json(), USER_SCHEMA)


def test_get_user_field_values(api, base_url):
    user = api.get(f"{base_url}/users/1").json()

    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
    assert user["username"] == "Bret"
    assert user["email"] == "Sincere@april.biz"
    assert user["address"]["city"] == "Gwenborough"


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_get_existing_users_by_id(api, base_url, user_id):
    response = api.get(f"{base_url}/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


# ---------- POST /users ----------

def test_create_user(api, base_url):
    new_user = {
        "name": "Иван Петров",
        "username": "ivan_petrov",
        "email": f"ivan.petrov.{int(time.time() * 1000)}@example.com",
    }

    response = api.post(f"{base_url}/users", json=new_user)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["id"] == 11
    assert body["name"] == new_user["name"]
    assert body["username"] == new_user["username"]
    assert body["email"] == new_user["email"]


# ---------- PUT /users/{id} ----------

def test_update_user(api, base_url):
    updated = {
        "id": 1,
        "name": "Пётр Сидоров",
        "username": "petr_sidorov",
        "email": "petr.sidorov@example.com",
    }

    response = api.put(f"{base_url}/users/1", json=updated)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == updated["name"]
    assert body["username"] == updated["username"]
    assert body["email"] == updated["email"]
    # PUT заменяет ресурс целиком, поэтому старого поля address нет
    assert "address" not in body


# ---------- Негативный сценарий ----------

@pytest.mark.parametrize("user_id", [0, 11, 9999])
def test_get_nonexistent_user_returns_404(api, base_url, user_id):
    response = api.get(f"{base_url}/users/{user_id}")

    assert response.status_code == 404
    assert response.json() == {}
