import io
import os
import qrcode

import barcode
from barcode.writer import ImageWriter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_barcode_and_qrcode(barcode_value, qcode=False, webpage_link=None, bcode=True):

    barcode_path = os.path.join('static', 'barcodes', f'{barcode_value}')
    code128 = barcode.get_barcode_class('code128')
    my_barcode = code128(barcode_value, writer=ImageWriter())
    my_barcode.save(barcode_path)

    if qcode:
        qr = qrcode.QRCode(version=1, box_size=3.5, border=.5)
        qr.add_data(webpage_link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = os.path.join('static', 'qrcodes', f'{barcode_value}')
        img.save(qr_path + '.png')

    return barcode_value


    ## Aother way of working but it will create svg image which won't be supported by pdf library
    # from barcode import Code128  
    # code128 = Code128(barcode_value)
    # code128.save(barcode_path)
