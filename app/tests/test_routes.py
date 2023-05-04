def test_read_all_planets_returns_empty_list(client):
    response = client.get("/planets")
    response_body = response.get_json()


    # assert
    assert response_body == []
    assert response.status_code == 200

def test_read_planet_by_id_returns_json(make_two_planets,client):
    response = client.get("/planets/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id" : 2,
        "name": "Mars",
        "description": "red planet"
    }

def test_read_planet_by_id_returns_not_found(make_two_planets,client):
    response = client.get("/planets/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message" : "Planet 3 does not exist."
    }

def test_create_a_planet(client):
    response = client.post("/planets", json={
        "name": "jupiter",
        "description": "big"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Yaaaaay planet jupiter has been made"

def test_read_all_planets_returns_planets(make_two_planets,client):
    response = client.get("/planets")
    response_body = response.get_json()


    # assert
    assert response_body == [
        {
            "id" : 1,
            "name" : "Earth",
            "description" : "our planet"}, 
        {
            "id" : 2,
            "name" : "Mars",
            "description": "red planet"}
        ]
    assert response.status_code == 200