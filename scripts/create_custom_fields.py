"""Create the UAE e-invoicing Custom Field records in ERPNext.

Run locally:
    pip install -r requirements.txt
    cp .env.example .env
    # edit .env with a newly generated API key and secret
    python scripts/create_custom_fields.py

The script is idempotent: existing fields are skipped. It does not create
standard ERPNext fields such as posting_date, currency, qty, rate, or tax_id.
"""

import os
import sys
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("ERPNEXT_URL", "").rstrip("/")
API_KEY = os.getenv("ERPNEXT_API_KEY", "")
API_SECRET = os.getenv("ERPNEXT_API_SECRET", "")

FIELDS: List[Dict] = [
    # Sales Invoice
    {"dt": "Sales Invoice", "label": "Invoice Type Code", "fieldname": "custom_invoice_type_code", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice", "label": "Invoice Transaction Type Code", "fieldname": "custom_transaction_type_code", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice", "label": "Business Process Type", "fieldname": "custom_business_process_type", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice", "label": "Specification Identifier", "fieldname": "custom_specification_identifier", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice", "label": "Payment Means Type Code", "fieldname": "custom_payment_means_type_code", "fieldtype": "Data", "reqd": 1},
    # Company
    {"dt": "Company", "label": "Seller Electronic Address", "fieldname": "custom_seller_electronic_address", "fieldtype": "Data", "reqd": 1},
    {"dt": "Company", "label": "Seller Electronic Identifier", "fieldname": "custom_seller_electronic_identifier", "fieldtype": "Data", "reqd": 1},
    {"dt": "Company", "label": "Seller Legal Registration Identifier", "fieldname": "custom_seller_legal_registration_identifier", "fieldtype": "Data", "reqd": 1},
    {"dt": "Company", "label": "Seller Legal Registration Identifier Type", "fieldname": "custom_seller_legal_registration_identifier_type", "fieldtype": "Data", "reqd": 1},
    {"dt": "Company", "label": "Seller Tax Scheme Code", "fieldname": "custom_seller_tax_scheme_code", "fieldtype": "Data", "reqd": 1},
    # Customer
    {"dt": "Customer", "label": "Buyer Electronic Address", "fieldname": "custom_buyer_electronic_address", "fieldtype": "Data", "reqd": 1},
    {"dt": "Customer", "label": "Buyer Electronic Identifier", "fieldname": "custom_buyer_electronic_identifier", "fieldtype": "Data", "reqd": 1},
    {"dt": "Customer", "label": "Buyer Legal Registration Identifier", "fieldname": "custom_buyer_legal_registration_identifier", "fieldtype": "Data", "reqd": 0},
    {"dt": "Customer", "label": "Buyer Tax Scheme Code", "fieldname": "custom_buyer_tax_scheme_code", "fieldtype": "Data", "reqd": 1},
    # Sales Taxes and Charges child table
    {"dt": "Sales Taxes and Charges", "label": "Taxable Amount", "fieldname": "custom_taxable_amount", "fieldtype": "Currency", "reqd": 1},
    {"dt": "Sales Taxes and Charges", "label": "Tax Category Code", "fieldname": "custom_tax_category_code", "fieldtype": "Data", "reqd": 1},
    # Sales Invoice Item child table
    {"dt": "Sales Invoice Item", "label": "Invoice Line Identifier", "fieldname": "custom_invoice_line_identifier", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice Item", "label": "Item Gross Price", "fieldname": "custom_item_gross_price", "fieldtype": "Currency", "reqd": 1},
    {"dt": "Sales Invoice Item", "label": "Item Price Base Quantity", "fieldname": "custom_price_base_quantity", "fieldtype": "Float", "reqd": 1},
    {"dt": "Sales Invoice Item", "label": "Invoiced Item Tax Category Code", "fieldname": "custom_invoiced_item_tax_category_code", "fieldtype": "Data", "reqd": 1},
    {"dt": "Sales Invoice Item", "label": "Invoiced Item Tax Rate", "fieldname": "custom_invoiced_item_tax_rate", "fieldtype": "Percent", "reqd": 1},
    {"dt": "Sales Invoice Item", "label": "VAT Line Amount", "fieldname": "custom_vat_line_amount", "fieldtype": "Currency", "reqd": 1},
]


def headers() -> Dict[str, str]:
    return {
        "Authorization": f"token {API_KEY}:{API_SECRET}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def validate_config() -> None:
    if not BASE_URL or not API_KEY or not API_SECRET:
        raise SystemExit("Set ERPNEXT_URL, ERPNEXT_API_KEY, and ERPNEXT_API_SECRET in .env")


def field_exists(field: Dict) -> bool:
    response = requests.get(
        f"{BASE_URL}/api/resource/Custom Field",
        headers=headers(),
        params={"filters": f'[["dt","=","{field["dt"]}"],["fieldname","=","{field["fieldname"]}"]]'},
        timeout=30,
    )
    response.raise_for_status()
    return bool(response.json().get("data"))


def create_field(field: Dict) -> None:
    if field_exists(field):
        print(f"SKIP  {field['dt']}.{field['fieldname']} (already exists)")
        return
    response = requests.post(
        f"{BASE_URL}/api/resource/Custom Field",
        headers=headers(),
        json=field,
        timeout=30,
    )
    if response.status_code >= 400:
        print(response.text, file=sys.stderr)
        response.raise_for_status()
    print(f"CREATE {field['dt']}.{field['fieldname']}")


def main() -> None:
    validate_config()
    for field in FIELDS:
        create_field(field)
    print("Done. Reload ERPNext before testing a draft Sales Invoice.")


if __name__ == "__main__":
    main()
