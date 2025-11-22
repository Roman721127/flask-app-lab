from flask import (
    render_template, request, redirect, url_for, 
    flash, session, make_response
)
from app.users import bp
from app.forms import LoginForm 
import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('users.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        remember = form.remember.data
        flash(f'Вітаємо, {session["username"]}! Ви успішно увійшли. Запам\'ятати: {remember}', 'success')
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
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))
    
    cookies = request.cookies 
    return render_template(
        'users/profile.html', 
        user=session['username'], 
        cookies=cookies
    )

@bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'Невідомо') 
    return render_template('users/hi.html', name=name, age=age)

@bp.route('/admin')
def admin():
    return render_template('users/hi.html', name="ADMINISTRATOR", age=45)

@bp.route('/set_theme/<theme>')
def set_theme(theme):
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    resp.set_cookie('theme', theme, expires=expires)
    
    flash(f'Тему змінено на "{theme}".', 'info')
    return resp

@bp.route('/set_cookie', methods=['POST'])
def set_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))
    
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    days = request.form.get('cookie_days')

    if key == 'session':
        flash('Ви не можете змінити cookie сесії!', 'danger')
        return redirect(url_for('users.profile'))
        
    if not key or not value:
        flash('Ключ та Значення є обов\'язковими.', 'danger')
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    
    try:
        if days and int(days) > 0:
            expires = datetime.datetime.now() + datetime.timedelta(days=int(days))
            resp.set_cookie(key, value, expires=expires)
            flash(f'Cookie "{key}" встановлено на {days} днів.', 'success')
        else:
            resp.set_cookie(key, value)
            flash(f'Сесійний cookie "{key}" встановлено.', 'success')
    except Exception as e:
        flash(f'Помилка при встановленні cookie: {e}', 'danger')

    return resp

@bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))

    cookie_key = request.form.get('cookie_key_del')
    resp = make_response(redirect(url_for('users.profile')))
    
    if cookie_key:
        if cookie_key == 'session':
             flash('Ви не можете видалити cookie сесії вручну. Натисніть "Вийти".', 'danger')
        else:
            resp.delete_cookie(cookie_key)
            flash(f'Cookie "{cookie_key}" було видалено.', 'info')
            
    return resp

@bp.route('/clear_cookies', methods=['POST'])
def clear_cookies():
    if 'username' not in session:
        flash('Будь ласка, увійдіть.', 'warning')
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    
    for key in request.cookies:
        if key != 'session':
            resp.delete_cookie(key)
            
    flash('Всі cookies (окрім сесії) було очищено.', 'info')
    return resp