# Built-in imports
import os
import random
import string
from datetime import datetime

# External imports
import pytz
from PIL import Image, ImageDraw, ImageFont


# Load bank settings via environment variables
BASE_BANK = os.environ.get("BASE_BANK", "DemoBank")


def generate_random_receipt_number():
    """Generate a random alphanumeric string of 16 characters."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


def create_transaction_receipt_image(
    from_number, receiver_key, amount, output_dir="/tmp"
):
    """
    Method to generate a dynamic Bank Receipt (comprobante) for a transaction.
    """

    # Generate bank validation number
    comprobante_no = generate_random_receipt_number()

    # Set the timezone for Bogotá, Colombia
    bogota_timezone = pytz.timezone("America/Bogota")

    # Get the current datetime in the Bogotá timezone
    current_datetime = datetime.now(bogota_timezone).strftime("%d %b %Y - %I:%M %p")

    # Load the base image (absolute path)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
    base_image_path = os.path.join(script_dir, BASE_BANK, "bank_image_template.png")

    # Open the base image
    image = Image.open(base_image_path)
    draw = ImageDraw.Draw(image)

    # Define positions for the text (scaled up)
    image_configurations = {
        "RufusBank": {
            "fill": "black",
            "title": (200, 550),  # Title position
            "comprobante_no": (150, 720),  # Comprobante No. position
            "datetime": (150, 770),  # Date and time position
            "from_number_label": (100, 950),  # "Producto Origen" label position
            "from_number_value": (100, 1000),  # Producto Origen value
            "receiver_key_label": (100, 1150),  # "Producto Destino" label position
            "receiver_key_value": (100, 1200),  # Producto Destino value
            "amount_label": (100, 1350),  # "Valor enviado" label position
            "amount_value": (100, 1400),  # Valor enviado value
            "font_title": ImageFont.load_default(size=70),
            "font_medium": ImageFont.load_default(size=40),
            "font_small": ImageFont.load_default(size=30),
            "font_x_small": ImageFont.load_default(size=30),
        },
    }

    # Write text onto the image
    draw.text(
        image_configurations[BASE_BANK]["title"],
        "Transferencia exitosa",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_title"],
    )
    draw.text(
        image_configurations[BASE_BANK]["comprobante_no"],
        f"Comprobante No: {comprobante_no}",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_medium"],
    )
    draw.text(
        image_configurations[BASE_BANK]["datetime"],
        current_datetime,
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_medium"],
    )
    draw.text(
        image_configurations[BASE_BANK]["from_number_label"],
        "Cuenta Ahorros:",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_small"],
    )
    draw.text(
        image_configurations[BASE_BANK]["from_number_value"],
        f"{from_number}",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_medium"],
    )
    draw.text(
        image_configurations[BASE_BANK]["receiver_key_label"],
        "Llave Bre-B Destinatario:",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_x_small"],
    )
    draw.text(
        image_configurations[BASE_BANK]["receiver_key_value"],
        f"{receiver_key}".upper(),
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_medium"],
    )
    draw.text(
        image_configurations[BASE_BANK]["amount_label"],
        "Valor enviado:",
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_small"],
    )

    # Format the amount safely
    try:
        formatted_amount = f"${float(amount):,} COP"
    except (ValueError, TypeError):
        formatted_amount = (
            f"${amount} COP"  # Use the original value if formatting fails
        )

    draw.text(
        image_configurations[BASE_BANK]["amount_value"],
        formatted_amount,
        fill=image_configurations[BASE_BANK]["fill"],
        font=image_configurations[BASE_BANK]["font_medium"],
    )

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the modified image
    output_path = os.path.join(output_dir, f"comprobante_{BASE_BANK}.png")
    image.save(output_path)

    return output_path


if __name__ == "__main__":
    from_number = "571234567890"
    receiver_key = "monitron123"
    amount = 1500000
    output_directory = "./temp"  # Change this to any desired directory
    create_transaction_receipt_image(
        from_number, receiver_key, amount, output_directory
    )
