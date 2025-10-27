from flask import render_template, request, redirect, url_for, flash, session, make_response
from app.users import bp

VALID_USER = {
    "username": "student",
    "password": "password123"
}
@bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'не вказано')
    return render_template('users/hi.html', name=name.upper(), age=age)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == VALID_USER['username'] and password == VALID_USER['password']:
            session['user'] = username
            flash("Вхід успішний.", "success")
            return redirect(url_for('users.profile'))
        else:
            flash("Невірне ім'я користувача або пароль.", "danger")
            return redirect(url_for('users.login'))
    return render_template('users/login.html', title="Login")


@bp.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        flash("Будь ласка, увійдіть перед переглядом профілю.", "warning")
        return redirect(url_for('users.login'))
    cookies = dict(request.cookies)
    theme = request.cookies.get('theme', 'light')
    return render_template('users/profile.html', title="Profile", user=user, cookies=cookies, theme=theme)


@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Ви вийшли з системи.", "info")
    return redirect(url_for('users.login'))


@bp.route('/profile/set_cookie', methods=['POST'])
def set_cookie():
    user = session.get('user')
    if not user:
        flash("Треба увійти.", "danger")
        return redirect(url_for('users.login'))

    key = request.form.get('cookie_key', '').strip()
    value = request.form.get('cookie_value', '').strip()
    days = int(request.form.get('cookie_days', 0) or 0)

    if not key:
        flash("Ключ cookie має бути заповнений.", "warning")
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    if days > 0:
        max_age = days * 24 * 60 * 60
        resp.set_cookie(key, value, max_age=max_age)
    else:
        resp.set_cookie(key, value)
    flash(f"Cookie '{key}' додано.", "success")
    return resp


@bp.route('/profile/delete_cookie', methods=['POST'])
def delete_cookie():
    user = session.get('user')
    if not user:
        flash("Треба увійти.", "danger")
        return redirect(url_for('users.login'))

    key = request.form.get('cookie_key_del', '').strip()
    resp = make_response(redirect(url_for('users.profile')))
    if key:
        resp.delete_cookie(key)
        flash(f"Cookie '{key}' видалено.", "info")
    else:
        flash("Не вказано ключ для видалення.", "warning")
    return resp


@bp.route('/profile/clear_cookies', methods=['POST'])
def clear_cookies():
    user = session.get('user')
    if not user:
        flash("Треба увійти.", "danger")
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    for key in request.cookies.keys():
        resp.delete_cookie(key)
    flash("Усі cookies видалено.", "info")
    return resp


@bp.route('/profile/theme/<theme>')
def set_theme(theme):
    user = session.get('user')
    if not user:
        flash("Треба увійти.", "danger")
        return redirect(url_for('users.login'))

    if theme not in ('light', 'dark'):
        flash("Невідома тема.", "warning")
        return redirect(url_for('users.profile'))

    resp = make_response(redirect(url_for('users.profile')))
    resp.set_cookie('theme', theme, max_age=30*24*60*60)
    flash(f"Тема змінена на {theme}.", "success")
    return resp
