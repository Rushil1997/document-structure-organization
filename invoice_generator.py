import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Circle, String

# Ensure output directory exists
os.makedirs('generated', exist_ok=True)

pdf_filename = "generated/invoice.pdf"
doc = SimpleDocTemplate(
    pdf_filename, 
    pagesize=letter,
    rightMargin=36, 
    leftMargin=36, 
    topMargin=36, 
    bottomMargin=36
)

styles = getSampleStyleSheet()

# --- Custom Styling System ---
title_style = ParagraphStyle(
    'InvoiceTitle',
    fontName='Helvetica-Bold',
    fontSize=36,
    leading=40,
    textColor=colors.HexColor('#1E2A5E') # Deep Slate Blue
)

company_style = ParagraphStyle(
    'CompanyDetails',
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#333333')
)

section_heading = ParagraphStyle(
    'SectionHeading',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#1E2A5E')
)

regular_text = ParagraphStyle(
    'RegularText',
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#333333')
)

table_header_style = ParagraphStyle(
    'TableHeader',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=12,
    textColor=colors.HexColor('#1E2A5E')
)

table_cell_style = ParagraphStyle(
    'TableCell',
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#333333')
)

table_cell_center = ParagraphStyle('TableCellCenter', parent=table_cell_style, alignment=1)
table_cell_right = ParagraphStyle('TableCellRight', parent=table_cell_style, alignment=2)

thank_you_style = ParagraphStyle(
    'ThankYou',
    fontName='Times-BoldItalic',
    fontSize=36,
    leading=40,
    textColor=colors.HexColor('#1E2A5E'),
    alignment=1
)

terms_title = ParagraphStyle(
    'TermsTitle',
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=12,
    textColor=colors.HexColor('#D9534F') # Accent Terracotta Crimson
)

story = []

# --- Header Section: Title and Placeholder Logo ---
logo_drawing = Drawing(80, 80)
logo_drawing.add(Circle(40, 40, 38, fillColor=colors.HexColor('#B0B3B8'), strokeColor=None))
logo_drawing.add(String(40, 34, "LOGO", fontName="Helvetica-Bold", fontSize=16, fillColor=colors.white, textAnchor="middle"))

header_table_data = [
    [Paragraph("INVOICE", title_style), logo_drawing]
]
header_table = Table(header_table_data, colWidths=[400, 140])
header_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
]))
story.append(header_table)

# --- Issuer Metadata ---
company_info = """<b>Zef Side Records</b><br/>
15 Bushwhack Road<br/>
Cape Town, Brits 3400"""
story.append(Paragraph(company_info, company_style))
story.append(Spacer(1, 20))

# --- Meta Segment Block (Bill To, Ship To, Core Meta Details) ---
meta_data = [
    [Paragraph("BILL TO", section_heading), Paragraph("SHIP TO", section_heading), Paragraph("INVOICE #", section_heading), Paragraph("ZA-001", regular_text)],
    [Paragraph("Vivian Fender", regular_text), Paragraph("Vivian Fender", regular_text), Paragraph("INVOICE DATE", section_heading), Paragraph("29/01/2019", regular_text)],
    [Paragraph("1401 Roger Street", regular_text), Paragraph("202 Mandela Drive", regular_text), Paragraph("P.O.#", section_heading), Paragraph("1830/2019", regular_text)],
    [Paragraph("Blouberg, Limpopo 4800", regular_text), Paragraph("Benoni, Gauteng 7681", regular_text), Paragraph("DUE DATE", section_heading), Paragraph("26/04/2019", regular_text)]
]
meta_table = Table(meta_data, colWidths=[180, 180, 100, 80])
meta_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(meta_table)
story.append(Spacer(1, 30))

# --- Main Itemized Data Table ---
items_data = [
    [Paragraph("QTY", table_header_style), Paragraph("DESCRIPTION", table_header_style), Paragraph("UNIT PRICE", ParagraphStyle('THR', parent=table_header_style, alignment=2)), Paragraph("AMOUNT", ParagraphStyle('THR2', parent=table_header_style, alignment=2))],
    [Paragraph("1", table_cell_center), Paragraph("Limited edition solid gold record", table_cell_style), Paragraph("1,700.00", table_cell_right), Paragraph("1,700.00", table_cell_right)],
    [Paragraph("2", table_cell_center), Paragraph("Protective vinyl record sleeve", table_cell_style), Paragraph("95.00", table_cell_right), Paragraph("190.00", table_cell_right)],
    [Paragraph("3", table_cell_center), Paragraph("Custom left handed guitar", table_cell_style), Paragraph("35.00", table_cell_right), Paragraph("105.00", table_cell_right)],
    ["", "", Paragraph("Subtotal", table_cell_right), Paragraph("1,995.00", table_cell_right)],
    ["", "", Paragraph("VAT 15.0%", table_cell_right), Paragraph("299.25", table_cell_right)],
    ["", "", Paragraph("<b>TOTAL</b>", ParagraphStyle('T1', parent=table_cell_right, fontSize=11)), Paragraph("<b>R2,294.25</b>", ParagraphStyle('T2', parent=table_cell_right, fontSize=12, textColor=colors.HexColor('#1E2A5E')))]
]

items_table = Table(items_data, colWidths=[50, 290, 100, 100])
items_table.setStyle(TableStyle([
    ('LINEABOVE', (0,0), (-1,0), 1.2, colors.HexColor('#D9534F')),  # Red bounding rule
    ('LINEBELOW', (0,0), (-1,0), 1.2, colors.HexColor('#D9534F')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story.append(items_table)
story.append(Spacer(1, 25))

# --- Authorization Signature ---
sig_data = [
    ["", Paragraph("K. Andrews", ParagraphStyle('Sig', fontName='Times-BoldItalic', fontSize=26, alignment=2))]
]
sig_table = Table(sig_data, colWidths=[340, 200])
story.append(sig_table)
story.append(Spacer(1, 35))

# --- Document Footer Split: Branding and Bank Mandate ---
terms_body = """Payment is due within 15 days<br/><br/>
Capitec Bank<br/>
Sort Code: 12-34-56<br/>
Account Number: 12345678"""

terms_cell_content = [
    Paragraph("TERMS & CONDITIONS", terms_title),
    Spacer(1, 6),
    Paragraph(terms_body, regular_text)
]

footer_data = [
    [Paragraph("Thank you", thank_you_style), terms_cell_content]
]
footer_table = Table(footer_data, colWidths=[270, 270])
footer_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEBEFORE', (1,0), (1,0), 1.5, colors.HexColor('#D9534F')), # Vertical structural left bar
    ('LEFTPADDING', (1,0), (1,0), 15),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(footer_table)

# Build PDF Document
doc.build(story)
