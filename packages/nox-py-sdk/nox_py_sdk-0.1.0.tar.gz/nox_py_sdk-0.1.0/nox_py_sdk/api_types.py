from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Colors:
    primary: str
    secondary: str
    text: str
    button: str
    textButton: str

@dataclass
class Checkout:
    id: int
    image: str
    image_type: str
    description: str
    price: float
    redirect_url: str
    is_enabled: bool
    theme_color: str
    payment_method: str
    colors: Colors
    created_at: str
    url_id: str
    code: Optional[str]
    txid: Optional[str]

@dataclass 
class CheckoutDetail:
    image: str
    description: str
    price: float
    redirect_url: str
    is_enabled: bool
    payment_method: str
    colors: Colors
    url_id: str
    code: str
    txid: str


@dataclass
class GetCheckoutsResponse:
    checkouts: List[Checkout]
    current_page: int
    total_pages: int

@dataclass
class CreateCheckoutData:
    colors: Colors
    price: float
    description: str
    redirect_url: str
    payment_method: str
    is_enabled: bool
    theme_color: str

@dataclass
class CreateCheckoutResponse:
    id: int
    url_id: str

@dataclass
class UpdateCheckoutData:
    change_image: Optional[bool] = None
    colors: Optional[Colors] = None
    price: Optional[float] = None
    description: Optional[str] = None
    redirect_url: Optional[str] = None
    payment_method: Optional[str] = None
    is_enabled: Optional[bool] = None
    theme_color: Optional[str] = None

@dataclass
class UpdateCheckoutResponse:
    detail: str

# API V2 types

@dataclass
class Account:
    name: str
    balance: float

@dataclass
class CreatePaymentData:
    method: str
    code: str
    amount: float
    type: Optional[str] = None
    pixkey: Optional[str] = None

@dataclass
class CreatePaymentResponse:
    method: str
    code: str
    amount: float
    qrcode: str
    qrcodebase64: str
    copypaste: str
    txid: str
    Status: str

@dataclass
class Payment:
    Method: str
    Status: str
    Code: str
    TxID: str
    Amount: float
    end2end: Optional[str]
    receipt: Optional[str]

@dataclass
class CreateCreditCardPaymentData:
    amount: float
    email: str
    code: str
    name: str
    cpf_cnpf: str
    expired_url: str
    return_url: str
    max_installments_value: float
    soft_descriptor_light: str

@dataclass
class CreateCreditCardPaymentResponse:
    id: str
    due_date: str
    currency: str
    email: str
    status: str
    total_cents: int
    order_id: str
    secure_id: str
    secure_url: str
    total: str
    created_at_iso: str

@dataclass
class CreditCardPayment:
    id: int
    status: str
    code: str
    txid: str
    amount: float
    created_at: str
    paid_at: Optional[str]
    canceled_at: Optional[str]
    customer_name: str
    customer_email: str
    customer_document: str
    merchant_id: int
    id_from_bank: str

@dataclass
class TransactionsRequestFilters:
    beginDate: Optional[str] = None
    endDate: Optional[str] = None
    method: Optional[str] = None
    status: Optional[str] = None
