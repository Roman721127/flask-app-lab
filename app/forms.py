from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, Regexp

class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача / Email', validators=[
        InputRequired(message="Це поле обов'язкове")
    ])
    
    password = PasswordField('Пароль', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])
    
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Ім'я має бути від 4 до 10 символів")
    ])

    email = StringField('Email', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Email(message="Некоректний email")
    ])

    phone = StringField('Телефон', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX")
    ])

    subject_choices = [
        ('1', 'Загальне питання'),
        ('2', 'Технічна підтримка'),
        ('3', 'Пропозиція про співпрацю')
    ]
    subject = SelectField('Тема', choices=subject_choices, validators=[
        InputRequired(message="Оберіть тему")
    ])

    message = TextAreaField('Повідомлення', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
    ])
    
    submit = SubmitField('Надіслати')