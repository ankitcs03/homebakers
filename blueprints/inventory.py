from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, send_file
from models import UniqueItem, InventoryItem, db, Order, NonSaleItem
from datetime import datetime
import io
import uuid
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from utility.utils import generate_barcode_and_qrcode
from utility.image_slip import create_slip
inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/add_item_to_inventory', methods=['GET', 'POST'])
def add_item_to_inventory():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    if request.method == 'POST':
        item_id = request.form['item']
        quantity = int(request.form['quantity'])
        manufacturing_date = datetime.strptime(request.form['manufacturing_date'], '%Y-%m-%d').date()
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()
        barcode_value = str(uuid.uuid4())[:8]  # Generate an 8-character long unique barcode
        
        inventory_item = InventoryItem.query.filter_by(unique_item_id=item_id, manufacturing_date=manufacturing_date, expiry_date=expiry_date).first()
        if inventory_item:
            inventory_item.quantity += quantity
        else:
            # Generate URL for item_detail.html /item_detail/<barcode>
            webpage_link = url_for('inventory.get_item_detail', barcode=barcode_value, _external=True)
            # generate barcode and qrcode
            barcode_image, qrcode_image = generate_barcode_and_qrcode(barcode_value, qcode=True,webpage_link=webpage_link, bcode=True)
            # generate the details slip image
            slip_image = create_slip(
                    item_name=UniqueItem.query.get(item_id).name,
                    item_price=UniqueItem.query.get(item_id).price, 
                    manufacturing_date=manufacturing_date.strftime('%Y-%m-%d'), 
                    expiry_date=expiry_date.strftime('%Y-%m-%d'), 
                    description=UniqueItem.query.get(item_id).description, 
                    barcode_value=barcode_value,
                    barcode_image=barcode_image,
                    qrcode_image=qrcode_image

                )
            inventory_item = InventoryItem(
                                            unique_item_id=item_id, 
                                            quantity=quantity, 
                                            manufacturing_date=manufacturing_date, 
                                            expiry_date=expiry_date, 
                                            barcode=barcode_value, 
                                            barcode_image=barcode_image, 
                                            qrcode_image=qrcode_image,
                                            slip_image=slip_image)
            db.session.add(inventory_item)
        

        db.session.commit()
        
        barcode_image_base64 = base64.b64encode(barcode_image).decode('utf-8')
        qrcode_image_base64 = base64.b64encode(qrcode_image).decode('utf-8')
        return jsonify(success=True, inventory_item={
            'id': inventory_item.id,
            'unique_item': {
                'name': inventory_item.unique_item.name
            },
            'quantity': inventory_item.quantity,
            'manufacturing_date': inventory_item.manufacturing_date.strftime('%Y-%m-%d'),
            'expiry_date': inventory_item.expiry_date.strftime('%Y-%m-%d'),
            'barcode': inventory_item.barcode,
            'barcode_image': barcode_image_base64,
            'qrcode_image': qrcode_image_base64
        })
    
    unique_items = UniqueItem.query.all()
    inventory_items = InventoryItem.query.all()
    return render_template('add_item_to_inventory.html', unique_items=unique_items, inventory_items=inventory_items)

@inventory_bp.route('/out_item')
def out_item():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    return render_template('out_item.html')

@inventory_bp.route('/get_item_by_barcode/<barcode>')
def get_item_by_barcode(barcode): 
    item = db.session.query(InventoryItem, UniqueItem).join(UniqueItem, InventoryItem.unique_item_id == UniqueItem.id).filter(InventoryItem.barcode == barcode).first()
    if item:
        inventory_item, unique_item = item
        return jsonify(success=True, item={
            'id': inventory_item.id,
            'name': unique_item.name,
            'barcode': inventory_item.barcode,
            'price': unique_item.price,
            'quantity': inventory_item.quantity,
            'description': unique_item.description,
            'manufacturing_date': inventory_item.manufacturing_date.strftime('%Y-%m-%d'),
            'expiry_date': inventory_item.expiry_date.strftime('%Y-%m-%d')
        })
    return jsonify(success=False, message='Item not found')

@inventory_bp.route('/item_detail/<barcode>')
def get_item_detail(barcode):
    item = db.session.query(InventoryItem, UniqueItem).join(UniqueItem, InventoryItem.unique_item_id == UniqueItem.id).filter(InventoryItem.barcode == barcode).first()
    if item:
        inventory_item, unique_item = item
        return render_template('item_detail.html', inventory_item=inventory_item, unique_item=unique_item)
    return "Item not found", 404

@inventory_bp.route('/checkout', methods=['POST'])
def checkout():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    basket = request.json
    for item in basket:
        inventory_item = InventoryItem.query.filter_by(barcode=item['barcode']).first()
        if inventory_item and inventory_item.quantity >= item['quantity']:
            inventory_item.quantity -= item['quantity']
            if inventory_item.quantity == 0:
                db.session.delete(inventory_item)
            if item['type'] == 'sale':
                order = Order(item_id=item['id'], item_name= item['name'], quantity=item['quantity'], total_price=item['total'])
                db.session.add(order)
            else:
                non_sale_item = NonSaleItem(item_id=item['id'], item_name=item['name'], quantity=item['quantity'], description=item['description'])
                db.session.add(non_sale_item)
        else:
            return jsonify(success=False, message='Insufficient quantity for item: ' + item['name'])
    db.session.commit()
    return jsonify(success=True)

@inventory_bp.route('/live_inventory')
def live_inventory():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    inventory_items = db.session.query(InventoryItem, UniqueItem).join(UniqueItem, InventoryItem.unique_item_id == UniqueItem.id).all()
    total_value = sum(unique_item.price * inventory_item.quantity for inventory_item, unique_item in inventory_items)
    return render_template('live_inventory.html', inventory_items=inventory_items, total_value=total_value)

@inventory_bp.route('/view_orders')
def view_orders():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))
    orders = Order.query.all()
    total_value = sum(order.total_price for order in orders)
    return render_template('view_orders.html', orders=orders, total_value=total_value)

@inventory_bp.route('/view_non_sale_items')
def view_non_sale_items():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))
    non_sale_items = NonSaleItem.query.all()
    total_value = sum(non_sale_item.quantity * UniqueItem.query.get(non_sale_item.item_id).price for non_sale_item in non_sale_items)
    return render_template('view_non_sale_items.html', non_sale_items=non_sale_items, total_value=total_value)


@inventory_bp.route('/search_product')
def search_product():
    return render_template('search_product.html')


@inventory_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    code_type = request.form['codeType']
    num_copies = int(request.form['numCopies'])
    barcode = request.form['selectedBarcode']
    preview = request.args.get('preview', 'false').lower() == 'true'

    # Query the InventoryItem to get the image data
    inventory_item = InventoryItem.query.filter_by(barcode=barcode).first()
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    rows, cols = 10, 4
    if code_type == 'detailslip':
        rows, cols = 3, 2
    cell_width = width / cols
    cell_height = height / rows

    for i in range(num_copies):
        row = i // cols
        col = i % cols
        x = col * cell_width
        y = height - (row + 1) * cell_height

        if code_type == 'barcode':
            image_data = inventory_item.barcode_image
        elif code_type == 'qrcode':
            image_data = inventory_item.qrcode_image
        elif code_type == 'detailslip':
            image_data = inventory_item.slip_image
        else:
            raise ValueError('Invalid code type')

        if image_data:
            image_buffer = io.BytesIO(image_data)
            image_reader = ImageReader(image_buffer)
            c.drawImage(image_reader, x + 10, y + 10, width=cell_width - 20, height=cell_height - 20)

        if (i + 1) % (rows * cols) == 0:
            c.showPage()

    c.save()
    buffer.seek(0)

    if preview:
        return send_file(buffer, mimetype='application/pdf')
    else:
        return send_file(buffer, as_attachment=True, download_name='codes.pdf', mimetype='application/pdf')