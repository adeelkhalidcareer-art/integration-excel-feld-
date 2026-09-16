# ERPNext UAE invoice setup

## Add the fields using code

1. Generate a new ERPNext API key and secret. Do not use a key that was previously shared in chat.
2. Copy `.env.example` to `.env`.
3. Put the new credentials in `.env`. Never commit `.env`.
4. Install dependencies:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

5. Run the idempotent setup script:

```bash
python scripts/create_custom_fields.py
```

The script creates only UAE custom fields through the `Custom Field` DocType. It skips fields that already exist. Standard ERPNext fields such as `posting_date`, `currency`, `due_date`, `qty`, `uom`, `rate`, `net_amount`, `tax_amount`, `base_amount`, `tax_id`, and totals are not recreated.

## Excel template

Open `templates/uae_tax_invoice_template.csv` in Excel. Enter one invoice-line per row. If an invoice has multiple lines, repeat the invoice-level values on each row and change the line fields. Save as `.xlsx` if your importer requires Excel format.

The template contains all 51 mandatory columns. The example values are placeholders and must be replaced with your actual UAE/ASP-approved values.

## Important

Run the first test against a draft invoice workflow. Do not make all custom fields required until your ERPNext data and ASP rules are confirmed; required fields can prevent saving existing invoices. Verify the final UAE code lists, tax categories, and identifier schemes with your ASP.
