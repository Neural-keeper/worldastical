import pytest

import app as app_module


class FakeCache:
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key)

    def setex(self, key, _ttl, value):
        self.values[key] = value

    def delete(self, *keys):
        for key in keys:
            self.values.pop(key, None)


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(app_module, "LOCAL_DB", tmp_path / "test-worlds.db")
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        response = test_client.post(
            "/register", data={"username": "test_user", "password": "password123"}
        )
        assert response.status_code == 302
        yield test_client


def create_world(client, name="Test World"):
    response = client.post("/worlds", data={"name": name})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/worlds/{name}/Name")
    return name


def current_test_user_id():
    return app_module.user_by_username("test_user")["id"]


def test_health_check(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_world_cache_is_invalidated_after_save(client, monkeypatch):
    cache = FakeCache()
    monkeypatch.setattr(app_module, "CACHE", cache)
    name = "Cache World"
    client.post("/worlds", data={"name": name})
    user_id = current_test_user_id()

    app_module.load_worlds(user_id)
    app_module.load_world(name, user_id)
    assert cache.values

    world = app_module.load_world(name, user_id)
    app_module.save_world(name, world, user_id)

    assert cache.values == {}


def test_worlds_require_authentication(client):
    client.post("/logout")

    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_create_world_starts_at_name_section(client):
    create_world(client)

    response = client.get("/worlds/Test%20World/Name")

    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"Save and Next" in response.data


def test_duplicate_world_names_are_rejected_case_insensitively(client):
    create_world(client, "Elaria")

    response = client.post("/worlds", data={"name": "elaria"})

    assert response.status_code == 409
    assert len(app_module.load_worlds(current_test_user_id())) == 1


def test_invalid_world_name_returns_a_validation_message(client):
    response = client.post("/worlds", data={"name": "<script>"})

    assert response.status_code == 400
    assert b"World name may use letters" in response.data
    assert app_module.load_worlds(current_test_user_id()) == []


def test_missing_inspiration_is_rejected(client):
    name = create_world(client)

    response = client.post(
        f"/worlds/{name}/Inspiration",
        data={"known": "Yes", "value": "", "action": "save"},
    )

    assert response.status_code == 400
    assert b"Enter an inspiration or choose No" in response.data
    assert app_module.load_world(name, current_test_user_id())["Inspiration"] == ""


def test_invalid_geology_scale_is_rejected(client):
    name = create_world(client)

    response = client.post(
        f"/worlds/{name}/Geology",
        data={"scale": "Planetary", "places": "", "action": "save"},
    )

    assert response.status_code == 400
    assert b"Choose Small or Large" in response.data


def test_next_button_follows_all_ten_sections(client):
    name = create_world(client)
    current_section = app_module.SECTIONS[0]

    for next_section in app_module.SECTIONS[1:]:
        response = client.post(
            f"/worlds/{name}/{current_section}",
            data={"value": "saved", "action": "next"},
        )

        assert response.status_code == 302
        assert response.headers["Location"].endswith(f"/{next_section}")
        current_section = next_section

    assert current_section == "Quirk"


def test_geology_and_political_geography_keep_nested_values(client):
    name = create_world(client)

    geology_response = client.post(
        f"/worlds/{name}/Geology",
        data={
            "scale": "Large",
            "places": "Cliffs of Moher\nThe Glass Sea",
            "action": "save",
        },
    )
    political_response = client.post(
        f"/worlds/{name}/Political%20Geography",
        data={
            "countries": "Elaria: sharp cliffs\nVeyra: floating cities",
            "borders": "Elaria - Veyra: mountain pass",
            "action": "save",
        },
    )

    assert geology_response.status_code == 200
    assert political_response.status_code == 200
    saved_world = app_module.load_world(name, current_test_user_id())
    assert saved_world["Geology"] == {
        "Scale": "Large",
        "Places": ["Cliffs of Moher", "The Glass Sea"],
    }
    assert saved_world["Political Geography"]["Countries"] == [
        "Elaria: sharp cliffs",
        "Veyra: floating cities",
    ]
    assert saved_world["Political Geography"]["Borders"] == [
        "Elaria - Veyra: mountain pass",
    ]


def test_saved_world_can_be_reopened_with_persisted_content(client):
    name = create_world(client)
    client.post(
        f"/worlds/{name}/Inspiration",
        data={"known": "Yes", "value": "Medieval Europe", "action": "save"},
    )

    response = client.get(f"/worlds/{name}/Inspiration")

    assert response.status_code == 200
    assert b"Medieval Europe" in response.data


def test_inspiration_period_is_saved_when_no_inspiration_is_known(client):
    name = create_world(client)
    client.post(
        f"/worlds/{name}/Inspiration",
        data={"known": "No", "period": "Future", "action": "save"},
    )

    assert app_module.load_world(name, current_test_user_id())["Inspiration"] == "Future world inspiration"


def test_world_can_be_deleted(client):
    name = create_world(client)

    response = client.post(f"/worlds/{name}/delete")

    assert response.status_code == 302
    assert app_module.load_world(name, current_test_user_id()) is None
    assert client.get(f"/worlds/{name}").status_code == 302


def test_worlds_are_separated_between_users(client):
    create_world(client, "Private World")
    second_client = app_module.app.test_client()
    second_client.post(
        "/register", data={"username": "second_user", "password": "password123"}
    )

    assert b"Private World" not in second_client.get("/").data
    assert second_client.get("/worlds/Private%20World").status_code == 302
