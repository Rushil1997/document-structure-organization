from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Circle, String

from invoice import Invoice

# --- Colours ---
NAVY = colors.HexColor('#1E2A5E')
GREY_TEXT = colors.HexColor('#333333')
ACCENT = colors.HexColor('#D9534F')

# --- Styles (defined once, reused for every invoice) ---
title_style = ParagraphStyle('InvoiceTitle', fontName='Helvetica-Bold', fontSize=36, leading=40, textColor=NAVY)
company_style = ParagraphStyle('CompanyDetails', fontName='Helvetica', fontSize=10, leading=14, textColor=GREY_TEXT)
section_heading = ParagraphStyle('SectionHeading', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=NAVY)
regular_text = ParagraphStyle('RegularText', fontName='Helvetica', fontSize=9, leading=13, textColor=GREY_TEXT)
small_text = ParagraphStyle('SmallText', parent=regular_text, fontSize=7, leading=9)
table_header = ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=NAVY)
table_header_right = ParagraphStyle('TableHeaderRight', parent=table_header, alignment=2)
table_cell = ParagraphStyle('TableCell', fontName='Helvetica', fontSize=10, leading=14, textColor=GREY_TEXT)
table_cell_center = ParagraphStyle('TableCellCenter', parent=table_cell, alignment=1)
table_cell_right = ParagraphStyle('TableCellRight', parent=table_cell, alignment=2)
total_label = ParagraphStyle('TotalLabel', parent=table_cell_right, fontSize=11)
total_value = ParagraphStyle('TotalValue', parent=table_cell_right, fontSize=12, textColor=NAVY)
thank_you_style = ParagraphStyle('ThankYou', fontName='Times-BoldItalic', fontSize=36, leading=40, textColor=NAVY, alignment=1)
terms_title = ParagraphStyle('TermsTitle', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=ACCENT)


# --- Formatting helpers ---
def money(value):
    """Decimal -> '36,190.50'"""
    return f"{value:,.2f}"


def fmt_date(d):
    """date -> '27/01/2026'"""
    return d.strftime("%d/%m/%Y")


def address_lines(address):
    """'12 Oak Avenue, Greenwood, Johannesburg, 2021' -> one line per part."""
    return "<br/>".join(part.strip() for part in address.split(","))


# --- Sections: each takes the invoice and RETURNS its piece of the PDF ---
def build_header():
    logo = Drawing(80, 80)
    logo.add(Circle(40, 40, 38, fillColor=colors.HexColor('#B0B3B8'), strokeColor=None))
    logo.add(String(40, 34, "LOGO", fontName="Helvetica-Bold", fontSize=16,
                    fillColor=colors.white, textAnchor="middle"))

    table = Table([[Paragraph("INVOICE", title_style), logo]], colWidths=[400, 123])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    return table


def build_company_info(invoice):
    text = (f"<b>{invoice.company_name}</b><br/>"
            f"{address_lines(invoice.company_address)}<br/>"
            f"VAT No: {invoice.company_vat_number}")
    return Paragraph(text, company_style)


def build_meta_table(invoice):
    bill_to = (f"<b>{invoice.customer_trading_name}</b><br/>"
               f"VAT No: {invoice.customer_vat_number}")
    ship_to = address_lines(invoice.customer_shipping_address)
    po_number = invoice.purchase_order_number or "-"

    data = [
        [Paragraph("BILL TO", section_heading), Paragraph("SHIP TO", section_heading),
         Paragraph("INVOICE #", section_heading), Paragraph(invoice.number, regular_text)],
        [Paragraph(bill_to, regular_text), Paragraph(ship_to, regular_text),
         Paragraph("INVOICE DATE", section_heading), Paragraph(fmt_date(invoice.invoice_date), regular_text)],
        ["", "", Paragraph("P.O.#", section_heading), Paragraph(po_number, regular_text)],
        ["", "", Paragraph("DUE DATE", section_heading), Paragraph(fmt_date(invoice.due_date), regular_text)],
    ]
    table = Table(data, colWidths=[160, 180, 100, 83])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 1), (0, 3)),   # bill-to text spans the lower rows
        ('SPAN', (1, 1), (1, 3)),   # ship-to text spans the lower rows
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return table


def build_items_table(invoice):
    # Header row
    rows = [[
        Paragraph("QTY", table_header),
        Paragraph("DESCRIPTION", table_header),
        Paragraph("UNIT PRICE", table_header_right),
        Paragraph("AMOUNT", table_header_right),
    ]]

    # One row per line item -- this loop replaces the old hardcoded rows
    for item in invoice.items:
        rows.append([
            Paragraph(str(item.quantity), table_cell_center),
            Paragraph(item.name, table_cell),
            Paragraph(money(item.unit_price), table_cell_right),
            Paragraph(money(item.total_price), table_cell_right),
        ])

    # Totals rows
    rows.append(["", "", Paragraph("Subtotal", table_cell_right), Paragraph(money(invoice.subtotal), table_cell_right)])
    rows.append(["", "", Paragraph("VAT 15.0%", table_cell_right), Paragraph(money(invoice.vat_amount), table_cell_right)])
    rows.append(["", "", Paragraph("<b>TOTAL</b>", total_label), Paragraph(f"<b>R{money(invoice.total)}</b>", total_value)])

    table = Table(rows, colWidths=[50, 273, 100, 100])
    table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, ACCENT),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return table


def build_footer(invoice):
    terms_text = (invoice.terms_and_conditions or "").strip()
    terms_cell = [
        Paragraph("TERMS & CONDITIONS", terms_title),
        Spacer(1, 6),
        Paragraph(terms_text, small_text),
    ]
    table = Table([[Paragraph("Thank you", thank_you_style), terms_cell]], colWidths=[220, 303])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBEFORE', (1, 0), (1, 0), 1.5, ACCENT),
        ('LEFTPADDING', (1, 0), (1, 0), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return table


# --- Main function: puts the sections together in order ---
def render_invoice_pdf(invoice: Invoice, path: str):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = [
        build_header(),
        build_company_info(invoice),
        Spacer(1, 20),
        build_meta_table(invoice),
        Spacer(1, 30),
        build_items_table(invoice),
        Spacer(1, 35),
        build_footer(invoice),
    ]
    doc.build(story)
