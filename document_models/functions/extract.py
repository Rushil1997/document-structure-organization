import pdfplumber
import ollama
from invoice import Invoice


def read_pdf(path):
    with pdfplumber.open(path) as pdf:
        texts = []
        for page in pdf.pages:
            texts.append(page.extract_text(layout= True))
        return "\n".join(texts)


PROMPT = """Extract the invoice data from the text below.
Return only JSON. Remove commas and the "R" from amounts, but keep the decimal point.
Example: "R1,995.00" becomes 1995.00 and "300.25" stays 300.25.
Dates in the invoice are written as dd/mm/yyyy.
Output dates in YYYY-MM-DD format.
The company address must not include the VAT number.

Invoice text:
{text}
"""


def extract_invoice(text, model="qwen3:8b"):
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": PROMPT.format(text=text)}],
        format=Invoice.model_json_schema(),
        think=False,
        options={"temperature": 0},
    )
    json_reply = response.message.content
    return Invoice.model_validate_json(json_reply)


# text = read_pdf("generated/INV-0001.pdf")
# invoice = extract_invoice(text)
# print(invoice)


# True or False
FIELDS = ["number", "invoice_date", "due_date", "subtotal", "vat_amount", "total",
          "company_name", "company_vat_number", "customer_vat_number"]

scores = {}
for field in FIELDS:
    scores[field] = 0

for n in range(1, 21):
    pdf_path = f"generated/INV-{n:04d}.pdf"
    json_path = f"generated/INV-{n:04d}.json"

    extracted = extract_invoice(read_pdf(pdf_path))
    label = Invoice.model_validate_json(open(json_path).read())

    for field in FIELDS:
        if getattr(extracted, field) == getattr(label, field):
            scores[field] += 1

    print(f"Done INV-{n:04d}")

for field in FIELDS:
    print(f"{field}: {scores[field]}/20")