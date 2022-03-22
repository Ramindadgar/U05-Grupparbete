from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.main import app

# from unittest.mock import patch
# from pytest import raises
# import os

# from src.main import stores


client = TestClient(app)


#To runt pytest: docker-compose exec web pytest . -v
#-v (verbose, to get more info)


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
    "Gävle",
    "Falun",
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
    response = client.get("/city?zip=5555555")
    assert response.status_code == 404
    assert response.json() == {
  "detail": "No city was found"
}


def test_sales():    
    response = client.get("/sales")
    assert response.status_code == 200
    assert response.json() == {
  "data": [
    {
      "store": "Den Stora Djurbutiken",
      "timestamp": "2022-01-25T13:52:34",
      "sale_id": "0188146f-5360-408b-a7c5-3414077ceb59"
    },
    {
      "store": "Djuristen",
      "timestamp": "2022-01-26T15:24:45",
      "sale_id": "726ac398-209d-49df-ab6a-682b7af8abfb"
    },
    {
      "store": "Den Lilla Djurbutiken",
      "timestamp": "2022-02-07T09:00:56",
      "sale_id": "602fbf9d-2b4a-4de2-b108-3be3afa372ae"
    },
    {
      "store": "Den Stora Djurbutiken",
      "timestamp": "2022-02-27T12:32:46",
      "sale_id": "51071ca1-0179-4e67-8258-89e34b205a1e"
    }
  ]
}


def test_specific_sale():
    response = client.get("/sales/0188146f-5360-408b-a7c5-3414077ceb59")
    assert response.status_code == 200
    assert response.json() == {
  "data": {
    "store": "Den Stora Djurbutiken",
    "timestamp": "2022-01-25T13:52:34",
    "sale_id": "0188146f-5360-408b-a7c5-3414077ceb59",
    "products": [
      {
        "name": "Hundmat",
        "qty": 3
      }
    ]
  }
}


def test_specific_sale_not_valid_entry():
    response = client.get("/sales/d546dfs6d54sdf65s4df6s5d4f654e")
    assert response.status_code == 422
    assert response.json() == {
  "detail": "Invalid entry"
}


def test_specific_sale_not_exist():
    response = client.get("/sales/0188146f-5360-408b-a7c5-3414077ceb80")
    assert response.status_code == 404
    assert response.json() == {
  "detail": "ID does not exist"
}


all_inventories = [
    [
        "Hundmat",
        27,
        "Den Lilla Djurbutiken"
    ],
    [
        "Kattmat",
        387,
        "Den Lilla Djurbutiken"
    ],
    [
        "Hundmat",
        140,
        "Den Stora Djurbutiken"
    ],
    [
        "Kattklonare",
        68,
        "Den Stora Djurbutiken"
    ],
    [
        "Kattmat",
        643,
        "Den Stora Djurbutiken"
    ],
    [
        "Sömnpiller och energidryck för djur",
        61,
        "Den Stora Djurbutiken"
    ],
    [
        "Elefantkoppel",
        27,
        "Djuristen"
    ],
]

return_data = [
  {
    "product_name": "Hundmat",
    "adjusted_quantity": 27,
    "store_name": "Den Lilla Djurbutiken"
  },
  {
    "product_name": "Kattmat",
    "adjusted_quantity": 387,
    "store_name": "Den Lilla Djurbutiken"
  },
  {
    "product_name": "Hundmat",
    "adjusted_quantity": 140,
    "store_name": "Den Stora Djurbutiken"
  },
  {
    "product_name": "Kattklonare",
    "adjusted_quantity": 68,
    "store_name": "Den Stora Djurbutiken"
  },
  {
    "product_name": "Kattmat",
    "adjusted_quantity": 643,
    "store_name": "Den Stora Djurbutiken"
  },
  {
    "product_name": "Sömnpiller och energidryck för djur",
    "adjusted_quantity": 61,
    "store_name": "Den Stora Djurbutiken"
  },
  {
    "product_name": "Elefantkoppel",
    "adjusted_quantity": 27,
    "store_name": "Djuristen"
  }
]

def db_mock(data):
    """This function returns a database mocking object, that will be used
    instead of the actual db connection.
    """
    database = SimpleNamespace()
    database.cursor = CursorMock(data)
    return database

class CursorMock:
    """This class mocks a db cursor. It does not build upon unittest.mock but
    it is instead built from an empty class, patching manually all needed
    methods.
    """
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __call__(self):
        return self

    @staticmethod
    def execute(*args):
        """This mocks cursor.execute. It returns args even though the return
        value of cursor.execute() is never used. This is to avoid the
        following linting error:

        W0613: Unused argument 'args' (unused-argument)
        """
        return args

    def fetchall(self):
        """This mocks cursor.fetchall.
        """
        return self.data


def test_get_inventory():
    """This unit test checks a call to GET /inventory without any query
    parameters.
    """
    app.db = db_mock(all_inventories)
    client = TestClient(app)
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == return_data


def test_get_inventory_store():
    """This unit test checks a call to GET /inventory?store=UUID
    """
    data = list(filter(lambda x: x[-1] == "Den Stora Djurbutiken",
                       all_inventories))
    app.db = db_mock(data)
    client = TestClient(app)
    response = client.get("/inventory",
                          params={
                              "store": "676df1a1-f1d1-4ac5-9ee3-c58dfe820927"})
    assert response.status_code == 200
    assert response.json() == list(filter(
        lambda x: x["store_name"] == "Den Stora Djurbutiken", return_data))

def test_get_inventory_product():
    """This unit test checks a call to GET /inventory?product=UUID
    """
    data = list(filter(lambda x: x[0] == "Hundmat", all_inventories))
    app.db = db_mock(data)
    client = TestClient(app)
    response = client.get("/inventory",
                          params={
                              "product": "a37c34ae-0895-484a-8b2a-355aea3b6c44"
                          })
    assert response.status_code == 200
    assert response.json() == list(filter(
        lambda x: x["product_name"] == "Hundmat", return_data))


def test_get_inventory_store_and_product():
    """This unit test checks a call to GET /inventory?store=UUID&product=UUID
    """
    data = list(filter(
        lambda x: x[0] == "Hundmat" and x[-1] == "Den Stora Djurbutiken",
        all_inventories))
    app.db = db_mock(data)
    client = TestClient(app)
    response = client.get("/inventory", params={
        "product": "a37c34ae-0895-484a-8b2a-355aea3b6c44",
        "store": "676df1a1-f1d1-4ac5-9ee3-c58dfe820927"
    })
    assert response.status_code == 200
    assert response.json() == list(
        filter(
            lambda x: x["store_name"] == "Den Stora Djurbutiken" and
                      x["product_name"] == "Hundmat", return_data))


def test_get_inventory_erroneous_store():
    """This unit test checks for a call to GET /inventory?store=Erroneous-UUID
    """
    app.db = db_mock(None)
    client = TestClient(app)
    response = client.get("/inventory",
                          params={"store": "this is not a valid UUID!"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID for store!"}


def test_get_inventory_erroneous_product():
    """This unit test checks for a call to GET /inventory?product=Erroneous-UUID
    """
    app.db = db_mock(None)
    client = TestClient(app)
    response = client.get("/inventory",
                          params={"product": "this is not a valid UUID!"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID for product!"}
