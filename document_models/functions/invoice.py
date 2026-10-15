from pydantic import BaseModel
from decimal import Decimal
from datetime import date 
from typing import Optional


class LineItem(BaseModel):
    name:str
    quantity: int
    unit_price: Decimal
    total_price: Decimal  # Formula = quantity x unit_price
    currentcy: str = 'ZAR'

class Invoice(BaseModel):
    number: str 
    vat_amount : Decimal
    subtotal: Decimal
    total: Decimal
    invoice_date:date
    due_date:date
    items: list[LineItem]
    purchase_order_number: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    company_name:str 
    company_address: str
    company_vat_number: str 
    customer_trading_name: str 
    customer_vat_number: str 
    customer_shipping_address: str 
    