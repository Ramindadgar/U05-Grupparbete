from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# To runt pytest: docker-compose exec web pytest . -v
# -v (verbose, to get more info)


def test_stores():    
    response = client.get("/stores")
    assert response.status_code == 200
    assert response.json() == {
  "data": [
    {
      "name": "Djurjouren",
      "address": "Upplandsgatan 99, 12345 Stockholm"
    },
    {
      "name": "Djuristen",
      "address": "Skånegatan 420, 54321 Falun"
    },
    {
      "name": "Den Lilla Djurbutiken",
      "address": "Nätverksgatan 22, 55555 Hudiksvall"
    },
    {
      "name": "Den Stora Djurbutiken",
      "address": "Routergatan 443, 54545 Hudiksvall"
    },
    {
      "name": "Noahs Djur & Båtaffär",
      "address": "Stallmansgatan 666, 96427 Gävle"
    }
  ]
}
    

def test_store_address():
    response = client.get("/stores/Djuristen")
    assert response.status_code == 200
    assert response.json() == {
  "data": {
    "name": "Djuristen",
    "address": "Skånegatan 420, 54321 Falun"
  }
}


def test_store_address_non_existing():
    response = client.get("/stores/InfernoOnline")
    assert response.status_code == 404
    assert response.json() == {
  "detail": "No stores was found"
}


def test_city_name():
    response = client.get("/city")
    assert response.status_code == 200
    assert response.json() == {
  "data": [
    "Falun",
    "Gävle",
    "Stockholm",
    "Hudiksvall"
  ]
}


def test_get_one_city():
    response = client.get("/city?zip=12345")
    assert response.status_code == 200
    assert response.json() == {
  "data": [
    "Stockholm"
  ]
}


def test_city_name_non_existing():
    response = client.get("/city/55555555")
    assert response.status_code == 404
    assert response.json() == {
  'detail': 'Not Found'
}
