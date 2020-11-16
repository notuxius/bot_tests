from time import sleep

import requests


class BotChatAPI:
    def __init__(self, token):
        self.API_URL = "https://api.autofaq.ai/v1/setup"
        self.user_token = token

    def http_get(self, location, params=None):
        api_url = self.API_URL + location
        print("GET {}\n{}".format(api_url, params))
        headers = {"AUTOFAQ-User-Token": self.user_token}
        response = requests.get(api_url, params=params, headers=headers)
        print("GET response {}: {}".format(response.status_code, response.text))

        assert response.status_code == 200, "unexpected status {}:\n {}".format(
            response.status_code, response.text
        )

        return response.json()

    def http_post(self, location, params=None):
        api_url = self.API_URL + location
        print("POST {}\n{}".format(api_url, params))
        print(self.user_token)
        headers = {"AUTOFAQ-User-Token": self.user_token}
        response = requests.post(api_url, json=params, headers=headers)
        print("POST response {}: {}".format(response.status_code, response.text))

        assert response.status_code == 200, "unexpected status {}:\n {}".format(
            response.status_code, response.text
        )

        return response.json()

    def http_put(self, location, params=None):
        api_url = self.API_URL + location
        print("PUT {}\n{}".format(api_url, params))
        headers = {"AUTOFAQ-User-Token": self.user_token}
        response = requests.put(api_url, json=params, headers=headers)
        print("PUT response {}: {}".format(response.status_code, response.text))

        assert response.status_code == 200, "unexpected status {}:\n {}".format(
            response.status_code, response.text
        )

        return response.json()

    def http_delete(self, location, params=None):
        api_url = self.API_URL + location
        print(f"DELETE {api_url}")
        headers = {"AUTOFAQ-User-Token": self.user_token}
        response = requests.delete(api_url, json=params, headers=headers)
        print("DELETE response {}: {}".format(response.status_code, response.text))

        assert response.status_code == 200, "unexpected status {}:\n {}".format(
            response.status_code, response.text
        )

        return response.json()
