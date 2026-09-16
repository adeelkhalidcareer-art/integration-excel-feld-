# integration-excel-feld-
businesses using ERP or accounting software often lack the mandatory fields required for e-invoicing. They need a simple connector that extracts existing invoice data, adds missing tax, customer, seller, item, and payment details, validates the invoice, sends it to an ASP, and returns the status without replacing their ERP.

## Overview

This project is a connector for UAE e-invoicing requirements. It reads invoice data from Excel, validates the 51 required fields, maps them into ERPNext, and creates the invoice in ERPNext through the REST API.

## ERPNext target

- Site URL: https://erpnext-lhs-xnd.k.frappe.cloud
- API endpoint: https://erpnext-lhs-xnd.k.frappe.cloud/api

## Folder structure

- `mappings/` — field mapping definitions
- `src/` — Python integration code
- `requirements.txt` — Python dependencies
- `.env.example` — credential template

## Quick start

1. Copy `.env.example` to `.env`
2. Fill in ERPNext API key and secret
3. Install requirements:
   `pip install -r requirements.txt`
4. Run the mapper:
   `python src/invoice_mapper.py`

## 51-field mapping scope

The project supports the UAE Standard Tax Invoice minimum mandatory fields, mapped to ERPNext objects:

- Sales Invoice = header + totals
- Customer = buyer
- Company = seller
- Address = buyer/seller address
- Item = item master
- Sales Invoice Item = invoice lines
- Sales Taxes and Charges = tax rows

## Field conventions

Any field ending in `custom_` must exist as a Custom Field in ERPNext before data is submitted.

## Notes

- Standard ERPNext totals are preferred over imported totals.
- Recalculate and validate tax before sending data to the ASP.
- Ensure UOM codes, tax codes, and tax categories comply with your ASP and UAE regulations.
