# Copyright 2025 Amazon Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Built-in imports
import os
import uuid
from datetime import datetime

# External imports
from fpdf import FPDF
import qrcode

# Own imports
from common.logger import custom_logger


logger = custom_logger()
BASE_BANK = os.environ.get("BASE_BANK", "RufusBank").upper()
QR_WEBSITE = os.environ.get("QR_WEBSITE", "https://example.com")
LOCATION = os.environ.get("LOCATION", "Medellín, Colombia")


def generate_certificate_pdf(product_list, location=LOCATION, output_path="/tmp"):
    """
    Function to generate a PDF certificate for a list of products.

    Args:
        product_list (list): List of products to generate the certificate for.
        location (str): Location to be included in the certificate.
        output_path (str): Path to save the generated PDF certificate.

    Returns:
        str: Path to the generated PDF certificate.
    """

    logger.info(f"Generating PDF certificate for {len(product_list)} products")
    logger.debug(f"Products list: {product_list}")

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(
                0, 10, f"{BASE_BANK} CERTIFICATE", border=False, ln=True, align="C"
            )
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    # Helper function to clean product data
    logger.info("Cleaning product data")

    def clean_product_data(product):
        cleaned = {}
        for key, value in product.items():
            if key == "PK":
                cleaned["User"] = value.split("#")[-1]  # Extract text after #
            elif key == "SK":
                continue  # Skip SK
            else:
                cleaned[key] = value
        return cleaned

    # Create a PDF instance
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add subtitle (generated time and location)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subtitle = f"Generado el: {generated_at}, Ubicación: {location}"

    for product in product_list:
        # Clean product data
        product_cleaned = clean_product_data(product)

        # Add a new page
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)

        # Subtitle
        pdf.cell(0, 10, subtitle, ln=True, align="C")
        pdf.ln(10)

        # Add product details as a table
        pdf.set_font("Arial", "", 10)
        col_width = pdf.w / 2.5  # Define column width
        row_height = 8  # Define row height
        for key, value in product_cleaned.items():
            pdf.cell(col_width, row_height, key, border=1)
            pdf.cell(col_width, row_height, str(value), border=1, ln=True)
        pdf.ln(10)

        # Generate QR Code
        qr_data = QR_WEBSITE
        qr_img = qrcode.make(qr_data)
        qr_filename = f"/tmp/{uuid.uuid4()}.png"
        qr_img.save(qr_filename)

        # Add QR Code to PDF
        pdf.image(qr_filename, x=10, y=pdf.get_y(), w=50)
        pdf.ln(55)  # Adjust line height after QR code

        # Add UUID
        unique_id = str(uuid.uuid4())
        pdf.cell(0, 10, f"UUID: {unique_id}", ln=True)

        # Remove temporary QR image
        os.remove(qr_filename)

    # Save the PDF
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{BASE_BANK}_extracto.pdf")
    pdf.output(output_file)
    logger.info(f"Successfully saved PDF file to {output_file}")

    return output_file


# Only for local tests/validations
if __name__ == "__main__":
    # Example usage
    product_list = [
        {
            "PK": "USER#santi123",
            "SK": "PRODUCT#01",
            "details": "Amex Card",
            "last_digits": "1111",
            "product_name": "Credit Card",
            "status": "ACTIVE",
        },
        {
            "PK": "USER#moni789",
            "SK": "PRODUCT#01",
            "details": "Visa Card",
            "last_digits": "2222",
            "product_name": "Debit Card",
            "status": "INACTIVE",
        },
    ]
    location = "Medellín, Colombia"
    generate_certificate_pdf(product_list, location, output_path="./temp")
