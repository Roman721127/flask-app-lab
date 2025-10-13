from flask import Flask, render_template
from config import SECRET_KEY, FLASK_DEBUG

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title="Моє резюме")


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
