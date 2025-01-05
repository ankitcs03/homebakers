import os
import base64
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from models import UniqueItem, db
import uuid
from utility.utils import generate_barcode_and_qrcode

unique_item_bp = Blueprint('unique_item', __name__)

@unique_item_bp.route('/add_unique_item', methods=['GET', 'POST'])
def add_unique_item():
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        description = request.form['description']
        barcode_value = str(uuid.uuid4())[:8]  # Generate an 8-character long unique barcode
        
        # barcode_value = generate_barcode_and_qrcode(barcode_value)
        barcode_image, qrcode_image = generate_barcode_and_qrcode(barcode_value, qcode=True)
        
        new_item = UniqueItem(name=item_name, price=price, description=description, barcode=barcode_value, barcode_image=barcode_image)
        db.session.add(new_item)
        db.session.commit()
        barcode_image_base64 = base64.b64encode(barcode_image).decode('utf-8')
        return jsonify(success=True, item={'id': new_item.id, 'name': item_name, 'price': price, 'description': description, 'barcode': barcode_value, 'barcode_image': barcode_image_base64})
    
    unique_items = UniqueItem.query.all()
    return render_template('add_unique_item.html', unique_items=unique_items)

@unique_item_bp.route('/get_unique_item/<int:item_id>', methods=['GET'])
def get_unique_item(item_id):
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    item = UniqueItem.query.get(item_id)
    if item:
        return jsonify(success=True, item={'id': item.id, 'name': item.name, 'price': item.price, 'description': item.description, 'barcode': item.barcode})
    return jsonify(success=False)

@unique_item_bp.route('/edit_unique_item/<int:item_id>', methods=['POST'])
def edit_unique_item(item_id):
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    item = UniqueItem.query.get(item_id)
    if item:
        item.name = request.form['item_name']
        item.price = request.form['price']
        item.description = request.form['description']
        db.session.commit()
        return jsonify(success=True, item={'id': item.id, 'name': item.name, 'price': item.price, 'description': item.description, 'barcode': item.barcode})
    return jsonify(success=False)

@unique_item_bp.route('/delete_unique_item/<int:item_id>', methods=['DELETE'])
def delete_unique_item(item_id):
    if not session.get('logged_in'):
        return redirect(url_for('user.login'))    
    item = UniqueItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        
        # Delete the barcode image
        barcode_path = os.path.join('static', 'barcodes', f'{item.barcode}.png')
        if os.path.exists(barcode_path):
            os.remove(barcode_path)

        return jsonify(success=True)
    return jsonify(success=False)