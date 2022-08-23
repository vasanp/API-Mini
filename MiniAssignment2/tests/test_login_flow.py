import requests
import pytest
from requests.structures import CaseInsensitiveDict


class TestLoginFlow:
    # class variables
    url = "https://hbs-ob-stage.herokuapp.com"
    value = 8122167122
    phone = "+91{}".format(value)
    name = "vasanth"
    email = "hasher@hashedin.com"
    password = "pass1"
    otp = 111111
    new_name = "P Vasanth"

    # checking status of website
    def test_check_status(self):
        # calling url
        response = requests.get(url="{}/status".format(self.url))
        # asserting status code
        assert response.status_code == 200
        # printing response
        print(response.text)

    # otp before registration
    def test_get_register_otp(self):
        # payload for request
        payload = {
            "phone": self.phone
        }
        # specific end point to hit
        endpoint = "{}/get_register_otp".format(self.url)
        # calling url
        response = requests.post(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 200
        assert response.json() == "OTP Sent to {}".format(self.phone)
        print(response.text)

    def test_create_user(self):
        # payload for request
        payload = {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "otp": self.otp
        }
        # specific end point to hit
        endpoint = "{}/user".format(self.url)
        # calling url
        response = requests.post(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 201
        assert response.json() == "User Created"
        print(response.text)

    def test_edit_user(self):
        # payload for request
        payload = {
            "name": self.new_name,
            "phone": self.phone,
            "email": self.email,
            "password": self.password,
            "otp": self.otp
        }
        # specific end point to hit
        endpoint = "{}/user".format(self.url)
        # sending request
        response = requests.put(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 200
        assert response.json() == "User Updated"
        print(response.text)

    def test_login_otp(self):
        # payload for request
        payload = {
            "phone": self.phone
        }
        # specific end point to hit
        endpoint = "{}/get_otp".format(self.url)
        # sending request
        response = requests.post(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 200
        assert response.json() is None
        print(response.text)

    def test_authenticate_password(self):
        # payload for request
        payload = {
            "phone": self.phone,
            "LoginType": "password",
            "password": self.password
        }
        # specific end point to hit
        endpoint = "{}/authenticate".format(self.url)
        # sending request
        response = requests.post(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 201
        jsonResponse = response.json()
        message = jsonResponse["message"]
        global access_token_password
        access_token_password = jsonResponse["access_token"]
        assert message == "User Logged in"
        print(message)

    def test_authenticate_otp(self):
        # payload for request
        payload = {
            "phone": self.phone,
            "LoginType": "OTP",
            "otp": self.otp
        }
        # specific end point to hit
        endpoint = "{}/authenticate".format(self.url)
        response = requests.post(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 201
        jsonResponse = response.json()
        message = jsonResponse["message"]
        access_token_otp = jsonResponse["access_token"]
        assert message == "User Logged in"
        print(message)

    def test_login(self):
        # sending header i.e. Bearer token with request to log in
        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Bearer {}".format(access_token_password)
        # specific end point to hit
        endpoint = "{}/protected_test".format(self.url)
        response = requests.get(url=endpoint, headers=headers)
        # asserting status code
        assert response.status_code == 200
        assert response.json() == "hello world"
        print(response.text)

    def test_delete_user(self):
        # payload for request
        payload = {
            "phone": self.phone,
            "otp": self.otp
        }
        # specific end point to hit
        endpoint = "{}/user".format(self.url)
        # sending request
        response = requests.delete(url=endpoint, json=payload)
        # asserting status code
        assert response.status_code == 200
        assert response.json() == "User deleted successfully"
        print(response.text)
