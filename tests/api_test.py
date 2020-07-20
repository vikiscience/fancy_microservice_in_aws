from http import HTTPStatus
import json
import pytest
import requests
import unittest


class MyAPITestCase(unittest.TestCase):
    api_url = 'http://localhost:8080'
    payload = {}

    def test_health(self):
        # send health request to app
        response = requests.get(self.api_url + '/healthcheck')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.text), {'message': 'Healthy'})

    def test_predict(self):
        response = requests.post(self.api_url + '/predict', json=self.payload)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(response.text), {'prediction': 0})


if __name__ == '__main__':
    # run tests with: python -m pytest tests/api_test.py
    # unittest.main()
    pytest.main()
