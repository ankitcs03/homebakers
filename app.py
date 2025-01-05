from config import Config
from flask import Flask, render_template, redirect, url_for, session
from flask_migrate import Migrate
from models import db, User
from blueprints.user import user_bp
from blueprints.unique_item import unique_item_bp
from blueprints.inventory import inventory_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(unique_item_bp)
app.register_blueprint(inventory_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username=app.config['USER_NAME']).first():
            root_user = User(username=app.config['USER_NAME'])
            root_user.set_password(app.config['USER_PASSWORD'])
            root_user.approved = True
            db.session.add(root_user)
            db.session.commit()
    app.run()
