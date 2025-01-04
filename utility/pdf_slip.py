from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
from textwrap import wrap

class GenerateDetailSlipPDF:

    def __init__(self, company_name, fssai_number, contact_details):
        self.company_name = company_name
        self.fssai_number = fssai_number
        self.contact_details = contact_details

    def create_slip(self, item_name, item_price, manufacturing_date, expiry_date, description, barcode_path, qrcode_path, num_copies):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        rows, cols = 3, 2
        cell_width = width / cols
        cell_height = height / rows

        # Register DejaVu Sans font
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
        c.setFont("DejaVuSans", 10)

        for i in range(num_copies):
            row = i // cols
            col = i % cols
            x = col * cell_width
            y = height - (row + .05) * cell_height + 5 * mm  # Adjusted starting position

            # Draw border
            c.setLineWidth(2)
            c.rect(x + 5 * mm, y - cell_height + 5 * mm, cell_width - 10 * mm, cell_height - 10 * mm)

            # Add company banner at the top
            banner_img_y = y - 5 * mm
            c.drawImage('static/images/slip-logo.png', x + 5 * mm, banner_img_y - 20 * mm, width=cell_width - 10 * mm, height=20 * mm)

            line_height = 12  # Reduced line height to save space
            current_y = banner_img_y - 25 * mm  # Adjusted starting position for content

            # Add barcode and QR code below the logo
            barcode_img_y = current_y - 15 * mm
            c.drawImage(barcode_path, x + 10 * mm, barcode_img_y, width=40 * mm, height=15 * mm)
            c.drawImage(qrcode_path, x + 70 * mm, barcode_img_y-5, width=20 * mm, height=20 * mm)  # Reduced QR code size

            current_y = barcode_img_y - 5 * mm  # Adjusted starting position for text content

            c.drawString(x + 10 * mm, current_y, f"Company Name: {self.company_name}")
            current_y -= line_height
            c.drawString(x + 10 * mm, current_y, f"FSSAI Licence Number: {self.fssai_number}")
            current_y -= line_height
            c.drawString(x + 10 * mm, current_y, f"Contact Details: {self.contact_details}")
            current_y -= line_height  
            c.drawString(x + 10 * mm, current_y, f"Item Name: {item_name}")
            current_y -= line_height
            c.drawString(x + 10 * mm, current_y, f"Item Price: ₹{item_price}")
            current_y -= line_height
            c.drawString(x + 10 * mm, current_y, f"MGF Date: {manufacturing_date}")
            current_y -= line_height
            c.drawString(x + 10 * mm, current_y, f"EXP Date: {expiry_date}")
            current_y -= line_height

            # Wrap description text with prefix
            description_text = f"Description: {description}"
            max_width = cell_width - 20 * mm
            wrapped_description = wrap(description_text, width=50)  # Adjust width as needed
            max_lines = 4
            for i, line in enumerate(wrapped_description[:max_lines]):
                if i == max_lines - 1 and len(wrapped_description) > max_lines:
                    # Remove the last word and add "..."
                    words = line.split()
                    truncated_line = " ".join(words[:-1]) + " ..."
                    c.drawString(x + 10 * mm, current_y, truncated_line)
                else:
                    c.drawString(x + 10 * mm, current_y, line)
                current_y -= line_height

            current_y -= line_height  # Add a line gap after contact details

            if (i + 1) % (rows * cols) == 0 and i != num_copies - 1:
                c.showPage()

        c.save()
        buffer.seek(0)
        return buffer
    
if __name__ == "__main__":
    # Example usage
    generator = GenerateDetailSlipPDF(company_name="Home Bakers", fssai_number="123456789", contact_details="Contact: YYY")
    buffer = generator.create_slip(
        item_name="Cake",
        item_price="500",
        manufacturing_date="2023-01-01",
        expiry_date="2023-01-10",
        description=" chocolate cake Delicious chocolate cake Delicious chocolate cake Delicious Delicious chocolate cake Delicious chocolate cake Delicious chocolate cake Delicious chocolate cake Delicious chocolate cake",
        barcode_path="static/barcodes/2a2afeb9.png",
        qrcode_path="static/qrcodes/2a2afeb9.png",
        num_copies=6
    )

    # Save the buffer to a file or send it as a response
    with open("detail_slips.pdf", "wb") as f:
        f.write(buffer.getbuffer())

