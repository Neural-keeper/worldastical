import pytest

import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(app_module, "LOCAL_DB", tmp_path / "test-worlds.db")
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client


def create_world(client, name="Test World"):
    response = client.post("/worlds", data={"name": name})
    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/worlds/{name}/Name")
    return name


def test_health_check(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_world_starts_at_name_section(client):
    create_world(client)

    response = client.get("/worlds/Test%20World/Name")

    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"Save and Next" in response.data


def test_duplicate_world_names_are_rejected_case_insensitively(client):
    create_world(client, "Elaria")

    response = client.post("/worlds", data={"name": "elaria"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    assert len(app_module.load_worlds()) == 1


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
    saved_world = app_module.load_world(name)
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

    assert app_module.load_world(name)["Inspiration"] == "Future world inspiration"


def test_world_can_be_deleted(client):
    name = create_world(client)

    response = client.post(f"/worlds/{name}/delete")

    assert response.status_code == 302
    assert app_module.load_world(name) is None
    assert client.get(f"/worlds/{name}").status_code == 302
