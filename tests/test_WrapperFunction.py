import unittest
from http import HTTPStatus

from fastapi.testclient import TestClient
from FastAPIApp import app
import azure.functions as func
from WrapperFunction import main


class TestFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_root(self) -> None:
        response = self.client.get("/")

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual({'message': f"Hello World"}, response.json())

    def test_say_hello_no_name(self) -> None:
        response = self.client.get("/hello/")

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual({'message': f"Hello noname"}, response.json())

    def test_say_hello_name(self) -> None:
        name = "IDNAP_team"
        response = self.client.get(f"/hello/{name}")

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual({'message': f"Hello {name}"}, response.json())

    def test_read_item(self) -> None:
        item_id = 4
        params = {'q': "val1"}
        response = self.client.get(f"/items/{item_id}/", params=params)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual({'item_id': item_id, 'q': params['q']}, response.json())

    def test_create_item(self) -> None:
        data = {'name': "NewItem", 'price': 12.34, 'is_offer': True}
        response = self.client.post(f"/items/", json=data)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(data, response.json())

    def test_patch_update_item(self) -> None:
        item_id = 2
        data = {'name': "NewPatchName", 'price': 34.12}
        response = self.client.patch(f"/items/{item_id}", json=data)
        response_data = data | {'is_offer': True}
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(response_data, response.json())

    def test_put_update_item(self) -> None:
        item_id = 2
        data = {'name': "NewPutName", 'price': 44.12}
        response = self.client.put(f"/items/{item_id}", json=data)
        response_data = data | {'is_offer': None}
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual(response_data, response.json())

    def test_delete_item(self) -> None:
        item_id = 3
        response = self.client.delete(f"/items/{item_id}")
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertDictEqual({'message': f"Item {item_id} deleted."}, response.json())
