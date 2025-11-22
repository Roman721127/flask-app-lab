from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import ContactForm

@app.route('/')
def resume():
    return render_template('resume.html', title="Резюме")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        
        flash(f'Дякуємо, {name}! Ваше повідомлення надіслано.', 'success')
        
        return redirect(url_for('contacts'))

    return render_template('contacts.html', title="Контакти", form=form)