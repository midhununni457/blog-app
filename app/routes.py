from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Midhun'}
    posts = [
        {
            'author': {'username': 'Midhun'},
            'body': "My first post!"
        },
        {
            'author': {'username': 'Ashwin'},
            'body': "Hi there!"
        },
    ]
    return render_template("index.html", title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested by {form.username.data}, remember me {form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)