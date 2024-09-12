import requests
from .api_types import (
    Account,
    CreatePaymentData,
    CreatePaymentResponse,
    Payment,
    CreateCreditCardPaymentData,
    CreateCreditCardPaymentResponse,
    CreditCardPayment,
    TransactionsRequestFilters
)

class V2Api:
    def __init__(self, api_token: str):
        self.base_url = "https://api2.noxpay.io"
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': api_token,
        }

    def get_account(self) -> Account:
        try:
            response = requests.get(f"{self.base_url}/account", headers=self.headers)
            response.raise_for_status()
            return Account(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def create_payment(self, data: CreatePaymentData) -> CreatePaymentResponse:
        try:
            response = requests.post(f"{self.base_url}/payment", headers=self.headers, json=data.__dict__)
            response.raise_for_status()
            return CreatePaymentResponse(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def create_payment_cash_out(self, data: CreatePaymentData) -> Payment:
        try:
            response = requests.post(f"{self.base_url}/payment", headers=self.headers, json=data.__dict__)
            response.raise_for_status()
            return Payment(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def get_payment(self, identifier: str) -> Payment:
        try:
            response = requests.get(f"{self.base_url}/payment/{identifier}", headers=self.headers)
            response.raise_for_status()
            return Payment(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def resend_webhook(self, txid: str) -> None:
        try:
            response = requests.get(f"{self.base_url}/payment/webhook/resend/{txid}", headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self._handle_error(e)

    def send_transactions_report(self, filters: TransactionsRequestFilters = {}) -> None:
        try:
            response = requests.post(f"{self.base_url}/report/transactions", headers=self.headers, json=filters.__dict__)
            response.raise_for_status()
        except requests.RequestException as e:
            self._handle_error(e)

    def create_credit_card_payment(self, data: CreateCreditCardPaymentData) -> CreateCreditCardPaymentResponse:
        try:
            response = requests.post(f"{self.base_url}/creditcard", headers=self.headers, json=data.__dict__)
            response.raise_for_status()
            return CreateCreditCardPaymentResponse(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def get_credit_card_payment(self, identifier: str) -> CreditCardPayment:
        try:
            response = requests.get(f"{self.base_url}/creditcard/{identifier}", headers=self.headers)
            response.raise_for_status()
            return CreditCardPayment(**response.json())
        except requests.RequestException as e:
            self._handle_error(e)

    def _handle_error(self, error: requests.RequestException):
        if error.response:
            raise Exception(f"API Error: {error.response.json().get('detail', error.response.text)}")
        else:
            raise Exception("API Error: No response received from the server.")
