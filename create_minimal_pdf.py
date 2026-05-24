#!/usr/bin/env python3
"""Create a minimal test PDF for Render memory testing."""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_minimal_pdf(filename="data/minimal_test.pdf"):
    """Create a 1KB minimal PDF."""
    os.makedirs("data", exist_ok=True)
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Bank Statement - Test")
    c.drawString(100, 730, "Account: 123456")
    c.drawString(100, 710, "Opening Balance: $1000")
    c.drawString(100, 690, "Closing Balance: $2000")
    c.save()
    size = os.path.getsize(filename)
    print(f"✓ Minimal PDF created: {filename} ({size} bytes)")

if __name__ == "__main__":
    create_minimal_pdf()
