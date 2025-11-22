from flask_wtf import FlaskForm
from wtforms import StringField,SelectField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectMultipleField, widgets
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

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Length(min=5, max=100, message="Заголовок має бути від 5 до 100 символів")
    ])
    content = TextAreaField('Вміст', validators=[
        InputRequired(message="Це поле обов'язкове")
    ])
    author = StringField('Автор', validators=[
        InputRequired(message="Вкажіть ім'я автора")
    ])
    submit = SubmitField('Зберегти')

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        InputRequired(message="Це поле обов'язкове"),
        Length(min=5, max=100, message="Заголовок має бути від 5 до 100 символів")
    ])
    content = TextAreaField('Вміст', validators=[
        InputRequired(message="Це поле обов'язкове")
    ])
    author = StringField('Автор', validators=[
        InputRequired(message="Вкажіть ім'я автора")
    ])

    category = SelectField('Категорія', coerce=int)
    
    tags = SelectMultipleField('Теги', coerce=int)
    
    submit = SubmitField('Зберегти')

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

    