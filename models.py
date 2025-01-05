from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    approved = db.Column(db.Boolean, default=False)  # New field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class UniqueItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    barcode = db.Column(db.String(8), unique=True, nullable=False)
    barcode_image = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return f'<UniqueItem {self.name} - {self.barcode}>'

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_item_id = db.Column(db.Integer, db.ForeignKey('unique_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacturing_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    barcode = db.Column(db.String(8), unique=True, nullable=False) 
    barcode_image = db.Column(db.LargeBinary, nullable=True)
    qrcode_image = db.Column(db.LargeBinary, nullable=True)
    slip_image = db.Column(db.LargeBinary, nullable=True)
    unique_item = db.relationship('UniqueItem', backref='inventory_items')

    def __repr__(self):
        return f'<InventoryItem {self.unique_item.name} - Quantity: {self.quantity}>'
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('unique_item.id'), nullable=False)
    item_name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    unique_item = db.relationship('UniqueItem')

    def __repr__(self):
        return f'<Order {self.unique_item.name} - Quantity: {self.quantity} - Total Price: {self.total_price}>'
    
class NonSaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('unique_item.id'), nullable=False)
    item_name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    unique_item = db.relationship('UniqueItem')

    def __repr__(self):
        return f'<NonSaleItem {self.unique_item.name} - Quantity: {self.quantity} - Description: {self.description}>'