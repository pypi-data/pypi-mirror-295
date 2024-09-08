import requests

from .exceptions import APIError, AuthenticationError, RateLimitError, ValidationError


class HTTPClient:
    def __init__(self, api_key, base_url="https://podscan.fm/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, params=params, json=data)

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 422:
            raise ValidationError(response.json().get("message", "Validation error"))
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code >= 400:
            raise APIError(
                f"API request failed: {response.text}",
                status_code=response.status_code,
                response=response,
            )

        return response.json()

    def get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self.request("POST", endpoint, data=data)

    def put(self, endpoint, data=None):
        return self.request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self.request("DELETE", endpoint)
