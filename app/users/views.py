from flask import render_template, request
from app.users import bp

@bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'не вказано')
    return render_template('users/hi.html', name=name.upper(), age=age)

@bp.route('/admin')
def admin():
    return render_template('users/hi.html', name='ADMINISTRATOR', age=45)
