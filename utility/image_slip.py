from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os
import io

class GenerateDetailSlipImage:

    def __init__(self, company_name, fssai_number, contact_details):
        self.company_name = company_name
        self.fssai_number = fssai_number
        self.contact_details = contact_details

    def create_slip_image(self, item_name, item_price, manufacturing_date, expiry_date, description, barcode_image, qrcode_image):
        # Define the size of each slip
        slip_width, slip_height = 297, 281  # A4 size divided by 2 columns and 3 rows

        # Create an image with white background
        image = Image.new('RGB', (slip_width, slip_height), 'white')
        draw = ImageDraw.Draw(image)

        # Load fonts
        font_path = 'static/fonts/DejaVuSans.ttf'
        font = ImageFont.truetype(font_path, 10)
        bold_font = ImageFont.truetype(font_path, 12)

        # Define positions and sizes
        margin = 10
        content_margin = 10  # Additional margin for content
        barcode_margin = 5
        qrcode_margin = 30
        line_height = 12
        current_y = margin

        # Draw border
        draw.rectangle([margin, margin, slip_width - margin, slip_height - margin], outline='black', width=2)

        # Add company banner at the top
        banner_img = Image.open('static/images/slip-logo.png')
        banner_img = banner_img.resize((slip_width - 2 * margin, 40))
        image.paste(banner_img, (margin, current_y))
        current_y += 45  # Adjust position after banner

        # Add barcode and QR code below the logo
        barcode_img = Image.open(io.BytesIO(barcode_image))
        barcode_img = barcode_img.resize((160, 60))
        image.paste(barcode_img, (margin + barcode_margin, current_y))
        
        qrcode_img = Image.open(io.BytesIO(qrcode_image))
        qrcode_img = qrcode_img.resize((60, 60))
        image.paste(qrcode_img, (margin + qrcode_margin + 170, current_y))
        current_y += 65  # Adjust position after barcode and QR code

        # Add text content
        draw.text((margin + content_margin, current_y), f"Company Name: {self.company_name}", font=bold_font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"FSSAI Licence Number: {self.fssai_number}", font=font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"Contact Details: {self.contact_details}", font=font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"Item Name: {item_name}", font=font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"Item Price: ₹{item_price}", font=font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"MGF Date: {manufacturing_date}", font=font, fill='black')
        current_y += line_height
        draw.text((margin + content_margin, current_y), f"EXP Date: {expiry_date}", font=font, fill='black')
        current_y += line_height

        # Wrap description text with prefix
        description_text = f"Description: {description}"
        max_width = slip_width - 2 * margin - content_margin
        wrapped_description = wrap(description_text, width=50)  # Adjust width as needed
        max_lines = 4
        for i, line in enumerate(wrapped_description[:max_lines]):
            if i == max_lines - 1 and len(wrapped_description) > max_lines:
                # Remove the last word and add "..."
                words = line.split()
                truncated_line = " ".join(words[:-1]) + " ..."
                draw.text((margin + content_margin, current_y), truncated_line, font=font, fill='black')
            else:
                draw.text((margin + content_margin, current_y), line, font=font, fill='black')
            current_y += line_height

        # # uncomment below code to Save the image in local directory, just full outputpath needed
        # image.save('static/images/test-slip.png', 'PNG')

        # Return the image buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        return image_buffer.getvalue()

def create_slip(item_name, item_price, manufacturing_date, expiry_date, description, barcode_value, barcode_image, qrcode_image):
    generator = GenerateDetailSlipImage(company_name="Home Bakers", fssai_number="123456789", contact_details="Contact: YYY")
    slip_image = generator.create_slip_image(
        item_name=item_name,
        item_price=item_price,
        manufacturing_date=manufacturing_date,
        expiry_date=expiry_date,
        description=description,
        barcode_image=barcode_image,
        qrcode_image=qrcode_image
    )
    return slip_image

# if __name__ == "__main__":
#     # Example usage
#     generator = GenerateDetailSlipImage(company_name="Home Bakers", fssai_number="123456789", contact_details="Contact: YYY")
#     with open("static/barcodes/2a2afeb9.png", "rb") as barcode_file, open("static/qrcodes/2a2afeb9.png", "rb") as qrcode_file:
#         barcode_image = barcode_file.read()
#         qrcode_image = qrcode_file.read()
#         generator.create_slip_image(
#             item_name="Cake",
#             item_price="500",
#             manufacturing_date="2023-01-01",
#             expiry_date="2023-01-10",
#             description="Delicious chocolate cake",
#             barcode_image=barcode_image,
#             qrcode_image=qrcode_image
#         )