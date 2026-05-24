"""
Create a sample bank statement PDF for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime, timedelta

# Create PDF
pdf_path = "data/sample_bank_statement.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []
styles = getSampleStyleSheet()

# Title
title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=18,
    textColor=colors.HexColor('#003366'),
    spaceAfter=6,
    alignment=1  # center
)
story.append(Paragraph("SAMPLE BANK STATEMENT", title_style))
story.append(Spacer(1, 0.2*inch))

# Account info
account_info = [
    "Account Holder: John Smith",
    f"Account Number: 1234567890",
    f"Statement Period: March 1, 2024 - March 31, 2024",
    f"Generated: {datetime.now().strftime('%B %d, %Y')}",
]
for line in account_info:
    story.append(Paragraph(line, styles['Normal']))
story.append(Spacer(1, 0.3*inch))

# Summary section
story.append(Paragraph("Account Summary", styles['Heading2']))
summary_data = [
    ["Opening Balance:", "$5,432.15"],
    ["Total Deposits:", "$8,250.00"],
    ["Total Withdrawals:", "-$3,125.50"],
    ["Closing Balance:", "$10,556.65"],
]
summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
summary_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(summary_table)
story.append(Spacer(1, 0.3*inch))

# Transactions
story.append(Paragraph("Transactions", styles['Heading2']))

transaction_data = [
    ["Date", "Description", "Withdrawal", "Deposit", "Balance"],
    ["03/01/2024", "Opening Balance", "", "$5,432.15", "$5,432.15"],
    ["03/02/2024", "Direct Deposit - Payroll", "", "$3,500.00", "$8,932.15"],
    ["03/04/2024", "Utility Payment", "-$125.50", "", "$8,806.65"],
    ["03/05/2024", "Grocery Store", "-$85.75", "", "$8,720.90"],
    ["03/08/2024", "Refund - Returned Item", "", "$250.00", "$8,970.90"],
    ["03/10/2024", "ATM Withdrawal", "-$300.00", "", "$8,670.90"],
    ["03/12/2024", "Restaurant", "-$47.23", "", "$8,623.67"],
    ["03/15/2024", "Direct Deposit - Payroll", "", "$3,500.00", "$12,123.67"],
    ["03/17/2024", "Insurance Payment", "-$250.00", "", "$11,873.67"],
    ["03/20/2024", "Gas Station", "-$45.75", "", "$11,827.92"],
    ["03/22/2024", "Online Purchase", "-$125.00", "", "$11,702.92"],
    ["03/25/2024", "Transfer In", "", "$250.00", "$11,952.92"],
    ["03/28/2024", "Monthly Fee", "-$50.00", "", "$11,902.92"],
    ["03/31/2024", "Interest Earned", "", "$3.73", "$10,556.65"],
]

transaction_table = Table(transaction_data, colWidths=[1*inch, 2.5*inch, 1*inch, 1*inch, 1*inch])
transaction_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(transaction_table)
story.append(Spacer(1, 0.3*inch))

# Footer
footer = "This is a sample bank statement for testing purposes only. Please keep this statement for your records."
story.append(Paragraph(footer, styles['Normal']))

# Build PDF
doc.build(story)
print(f"✓ Sample bank statement created at: {pdf_path}")
