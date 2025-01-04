from flask import Flask, render_template, redirect, url_for, session
from models import db, User
from blueprints.user import user_bp
from blueprints.unique_item import unique_item_bp
from blueprints.inventory import inventory_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(unique_item_bp)
app.register_blueprint(inventory_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='root').first():
            root_user = User(username='root')
            root_user.set_password('rootpassword')
            root_user.approved = True
            db.session.add(root_user)
            db.session.commit()
    app.run(debug=True)