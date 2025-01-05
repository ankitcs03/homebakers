# from ..config import Config
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from models import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('user.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please wait for approval.', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('user.login'))
        if not user.approved:
            flash('Your account is not approved yet!', 'danger')
            return redirect(url_for('user.login'))
        session['logged_in'] = True
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@user_bp.route('/admin')
def admin():
    if not session.get('logged_in') or session.get('username') != current_app.config['USER_NAME']:
        return redirect(url_for('user.login'))
    users = User.query.all()
    return render_template('admin.html', users=users, admin_username=current_app.config['USER_NAME'])

@user_bp.route('/approve_user/<int:user_id>')
def approve_user(user_id):
    if not session.get('logged_in') or session.get('username') != current_app.config['USER_NAME']:
        return redirect(url_for('user.login'))
    user = User.query.get(user_id)
    if user:
        user.approved = True
        db.session.commit()
        flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('user.admin'))

@user_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('logged_in') or session.get('username') != current_app.config['USER_NAME']:
        return redirect(url_for('user.login'))
    user = User.query.get(user_id)
    if user and user.username != current_app.config['USER_NAME']:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
    return redirect(url_for('user.admin'))