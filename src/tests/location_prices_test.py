import json
import unittest

from app.api import helper
from tests.app_test import test_app


def test_valid_price_calculation(test_app):
    data = {
        "zip_code": 10555,
        "city": "Nellischeid",
        "street": "Torstraße",
        "house_number": 26,
        "yearly_kwh_consumption": 1000
    }

    response = test_app.post("/prices/", data=json.dumps(data))

    assert response.status_code == 201
    assert response.json()['data']["unit_price"] == 1.66
    assert response.json()['data']["grid_fees"] == 3.99
    assert response.json()['data']["kwh_price"] == 0.58
    assert response.json()['data']["total_price"] == 585.65


def test_valid_price_calculation1(test_app):
    data = {
        "zip_code": 98954,
        "city": "Ost Auroraland",
        "street": "Kursiefen",
        "house_number": 15,
        "yearly_kwh_consumption": 1500
    }

    response = test_app.post("/prices/", data=json.dumps(data))

    assert response.status_code == 201
    assert response.json()['data']["unit_price"] == 2.30
    assert response.json()['data']["grid_fees"] == 3.53
    assert response.json()['data']["kwh_price"] == 0.62
    assert response.json()['data']["total_price"] == 935.83


def test_valid_multiplie_locations_price_calculation(test_app):
    data = {
        "zip_code": 86799,
        "city": 'Bad Annemarie',
        "street": 'Müritzstr.',
        "house_number": 50,
        "yearly_kwh_consumption": 1000
    }
    response = test_app.post("/prices/", data=json.dumps(data))
    assert response.status_code == 201
    assert response.json()['data']["unit_price"] == 3.15
    assert response.json()['data']["grid_fees"] == 1.24
    assert response.json()['data']["kwh_price"] == 0.68
    assert response.json()['data']["total_price"] == 684.39


def test_invalid_price_calculation(test_app):
    data = {
        "zip_code": 98954,
        "city": "Ost Auroraland",
        "house_number": 15,
        "yearly_kwh_consumption": 1500
    }

    response = test_app.post("/prices/", data=json.dumps(data))
    assert response.status_code == 422



class MissingLocationParameterTest(unittest.TestCase):

    # Returns True or False.
    def test_missing_location_parameter(self):
        data = {
            "zip_code": 98954,
            "city": "Ost Auroraland",
            "house_number": 15,
            "yearly_kwh_consumption": 1500
        }

        isValidLocation = helper.validateRequest(data)
        self.assertFalse(isValidLocation, False)

    # Returns True or False.
    def test_location_parameter(self):
        data = {
            "zip_code": 98954,
            "city": "Ost Auroraland",
            "street": "Kursiefen",
            "house_number": 15,
            "yearly_kwh_consumption": 1500
        }

        isValidLocation = helper.validateRequest(data)
        self.assertTrue(isValidLocation, True)