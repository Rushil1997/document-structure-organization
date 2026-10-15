import random as rd
from datetime import timedelta, date
from decimal import Decimal, ROUND_HALF_UP
from invoice import Invoice,LineItem
from render_invoice import render_invoice_pdf
import os


start_date = date(2026,1,1)


# Calculsting the VAT
VAT_RATE = Decimal("0.15")
PAYMENT_TERMS = 14

def add_vat(value):
    vat_amount = value * VAT_RATE
    total = vat_amount.quantize(Decimal('0.01'), ROUND_HALF_UP) + value


    return total

def total_amount(value):
    total = sum(value)
    total_including_vat =add_vat(total)
    return total_including_vat

#-----------------------------------------------------------------


terms_and_conditions  = """
Payment is due within 14 days of the invoice date via direct electronic funds transfer (EFT) in South African Rand (ZAR). Overdue balances will attract a late payment fee of 1.5% interest per month, accruing daily until the balance is settled in full. Any invoice disputes must be submitted in writing within 7 days of receipt, or the invoice will be deemed accepted as correct. All goods, services, or intellectual property deliverables remain the sole property of the provider until payment is received in full, and any associated usage rights may be suspended in the event of a default. Prices exclude VAT and other local taxes unless explicitly itemized, and the client is responsible for all applicable transaction or recovery fees.
"""
company_names = ['FHS','MFD','Investec','Discovery','Sasol','Nedbank']
addresses = [
    "12 Oak Avenue, Greenwood, Johannesburg, 2021",
    "84 Protea Street, Braamfontein, Johannesburg, 2001",
    "37 Marine Drive, Umhlanga Rocks, Durban, 4319",
    "55 Long Street, Cape Town CBD, Cape Town, 8001",
    "109 Jacaranda Crescent, Hatfield, Pretoria, 0083",
    "23 Baobab Boulevard, Nelspruit, 1200",
    "76 Main Road, Walmer, Gqeberha, 6070",
    "14 Mimosa Way, Welgemoed, Bellville, 7530",
    "92 Kingfisher Lane, Fourways, Sandton, 2055",
    "41 Beach Road, Summerstrand, Gqeberha, 6001"
]

shipping_addresses = [
    "Unit 4B, Industrial Park, 12 Falcon Road, Lanseria, 1748",
    "Suite 102, Willowbrook Office Park, Van Hoof Street, Ruimsig, 1724",
    "Plot 45, Old Pretoria Road, Midrand, 1685",
    "Warehouse 7, Mega Storage Facility, 88 Heidelberg Road, City Deep, 2049",
    "Building C, The Pivot, Montecasino Boulevard, Fourways, 2055",
    "Shop 14, Avalon Shopping Centre, 22 Robin Hood Road, Lenasia, 1827",
    "Unit 9, Highveld Techno Park, 44 Oak Avenue, Centurion, 0157",
    "Block A, Millennium Business Park, 19 Edison Way, Century City, 7441",
    "Unit 15, Northlands Deco Park, Phase 2, New Market Road, Northriding, 2169",
    "Warehouse B2, Riverhorse Valley Business Estate, 11 Riverhorse Close, Durban, 4017"
]


vat_numbers = [
    "0821234567",
    "0719876543",
    "0635551234",
    "0847778899",
    "0794445566",
    "0612223344",
    "0831112233",
    "0726667788",
    "0659990011",
    "0818889900"
]
filter_prices = {
    # Fuel & Engine Systems
    "P550388A": 150.25,
    "FF5052V": 300.25,
    "BF1212C": 500.00,
    "P55001T": 250.50,
    "CV5": 1500.00,
    "PA48": 200.00,
    "P5956": 8500.00,
    "UFGRG23101": 450.00,
    "Gfgdgdr12": 400.00,
    "WF23FD2071": 370.00,

    # Air Intake Systems
    "PUFC123828889": 900.00,
    "P834f@29333": 750.00,
    "AFRI12425126": 800.00,
    "PABBS1232820": 45.00,
    "P778542580": 120.00,
    "AFRI35325557": 500.00,
    "PANT1233493": 750.00,
    "POX23608675": 800.00,
    "AFRI232455815": 450.00,
    "PANT34A5690": 550.00,

    # Hydraulic Systems
    "POX23h550386": 850.00,
    "PANT238369": 550.00,
    "HFCS3rgr6510": 780.00,
    "PURTFG343550758": 650.00,
    "PERT12385T9413-MPG": 960.00,
    "ABC123": 450.00,
    "PWCfdd121": 780.00,
    "HEL24tgf": 785.45,
    "HFC2326162": 100.58,
    "POX2hfh3551551": 1000.00,

    # Transmission & Drivetrain
    "ddgdg97-HD": 782.00,
    "PANT235550387": 411.12,
    "HFCULefs28941": 780.00,
    "tesr1234": 1120.00,
    "FGD34": 788.00,
    "AB45": 52.12,
    "VB34": 78.00,
    "Pfsg34": 45.00,
    "Gwrw33": 45.00,

    # Engine Lubrication & Miscellaneous
    "TEs23": 500.00,
    "LFC!@#": 78.12,
    "TEST123": 800.00,
    "Hil@44": 960.00,
    "F122": 550.00,
    "AAA11": 410.00,
    "BB12": 980.00,
    "DAA2": 470.00,
    "TEFSF0dgs": 150.00,
    "Gefsfsg12": 120.00
}

def generate_line_items():
    number_of_items = rd.randint(1, 6)
    parts = rd.sample(list(filter_prices.keys()), number_of_items)

    items = []
    for part in parts:
        quantity = rd.randint(1, 10)
        unit_price = Decimal(str(filter_prices[part]))
        total_price = quantity * unit_price
        items.append(LineItem(name=part, quantity=quantity,
                              unit_price=unit_price, total_price=total_price))
    return items
def generate_invoice(n):
    invoice_number = f"INV-{n:04d}"
    invoice_date = start_date + timedelta(days=rd.randint(0, 365))
    due_date = invoice_date + timedelta(days=PAYMENT_TERMS)
    company_name = rd.choice(company_names)
    company_address = rd.choice(addresses)
    company_vat_number = rd.choice(vat_numbers)
    customer_vat_number = rd.choice(vat_numbers)
    customer_shipping_address = rd.choice(shipping_addresses)

    items = generate_line_items()

    subtotal = Decimal("0")
    for item in items:
        subtotal += item.total_price

    vat_amount = (subtotal * VAT_RATE).quantize(Decimal("0.01"), ROUND_HALF_UP)
    total = subtotal + vat_amount

    return Invoice(
        number=invoice_number,
        invoice_date=invoice_date,
        due_date=due_date,
        items=items,
        subtotal=subtotal,
        vat_amount=vat_amount,
        total=total,
        terms_and_conditions=terms_and_conditions,
        company_name=company_name,
        company_address=company_address,
        company_vat_number=company_vat_number,
        customer_trading_name=company_name,
        customer_vat_number=customer_vat_number,
        customer_shipping_address=customer_shipping_address,
    )

def save_invoice(invoice):
    path = f'generated/{invoice.number}.json'
    with open(path,'w') as f:
        f.write(invoice.model_dump_json(indent=2))


os.makedirs('generated',exist_ok=True)

  




for n in range(1, 21):
    invoice = generate_invoice(n)
    save_invoice(invoice)
    render_invoice_pdf(invoice, f'generated/{invoice.number}.pdf')

