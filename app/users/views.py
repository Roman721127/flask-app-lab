from flask import render_template, request, redirect, url_for, flash, session, make_response
from app import db
from app.users import bp
from app.forms import LoginForm
from app.models import User
import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('users.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        flash(f'Вітаємо, {session["username"]}!', 'success')
        return redirect(url_for('users.profile'))
    
    return render_template('users/login.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))
    
    username = session['username']
    user = db.session.scalar(db.select(User).where(User.username == username))
    cookies = request.cookies 
    
    return render_template('users/profile.html', user=user, cookies=cookies)

@bp.route('/set_theme/<string:theme>')
def set_theme(theme):
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    resp.set_cookie('theme', theme, expires=expires)
    
    return resp


@bp.route('/set_cookie', methods=['POST'])
def set_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    days = request.form.get('cookie_days')

    if key == 'session':
        flash('Не можна змінювати cookie сесії!', 'danger')
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    
    if days and int(days) > 0:
        expires = datetime.datetime.now() + datetime.timedelta(days=int(days))
        resp.set_cookie(key, value, expires=expires)
    else:
        resp.set_cookie(key, value)
    
    flash(f'Cookie "{key}" додано.', 'success')
    return resp

@bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
        
    key = request.form.get('cookie_key_del')
    resp = make_response(redirect(url_for('users.profile')))
    
    if key and key != 'session':
        resp.delete_cookie(key)
        flash(f'Cookie "{key}" видалено.', 'info')
    
    return resp

@bp.route('/clear_cookies', methods=['POST'])
def clear_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))
        
    resp = make_response(redirect(url_for('users.profile')))
    
    for key in request.cookies:
        if key != 'session':
            resp.delete_cookie(key)
            
    flash('Всі cookies очищено.', 'info')
    return resp

@bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'Невідомо')
    return render_template('users/hi.html', name=name, age=age)

@bp.route('/admin')
def admin():
    return render_template('users/hi.html', name="ADMINISTRATOR", age=45)