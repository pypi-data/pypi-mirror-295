import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .api_types import (
    Checkout,
    CheckoutDetail,
    GetCheckoutsResponse,
    CreateCheckoutData,
    CreateCheckoutResponse,
    UpdateCheckoutData,
    UpdateCheckoutResponse
)

class CheckoutApi:
    def __init__(self, token: str):
        self.base_url = "https://checkoutdev.noxpay.io"
        self.headers = {
            'Content-Type': 'application/json',
            'token': token,
        }

    def get_checkouts(self, query_params: dict = {}) -> GetCheckoutsResponse:
        try:
            response = requests.get(f"{self.base_url}/api/checkouts/", headers=self.headers, params=query_params)
            response.raise_for_status()
            return GetCheckoutsResponse(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def get_checkout(self, url_id: str) -> CheckoutDetail:
        try:
            response = requests.get(f"{self.base_url}/api/checkout-detail/{url_id}", headers=self.headers)
            response.raise_for_status()
            return CheckoutDetail(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def create_checkout(self, data: CreateCheckoutData, file=None) -> CreateCheckoutResponse:
        try:
            files = {'file': file} if file else {}
            data_dict = {'data': data.__dict__}
            response = requests.post(f"{self.base_url}/api/create-checkout/", headers=self.headers, files=files, data=data_dict)
            response.raise_for_status()
            return CreateCheckoutResponse(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def update_checkout(self, id: int, data: UpdateCheckoutData, file=None) -> UpdateCheckoutResponse:
        try:
            fields = {
                'data': (None, json.dumps(data), 'application/json')
            }
            if file:
                fields['file'] = (file.name, file, 'application/octet-stream')

            encoder = MultipartEncoder(fields=fields)
            headers = {
                'token': self.headers.get('token'),
                'Content-Type': encoder.content_type,
            }

            response = requests.put(f"{self.base_url}/api/update-checkout/{id}", headers=headers, data=encoder)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.RequestException):
        if error.response.text:
            raise Exception(f"API Error: {error.response.json().get('detail', error.response.text)}")
        else:
            raise Exception("API Error: No response received from the server.")
