from flask import request, session, redirect, url_for, \
     abort, render_template, flash

from flaskr import app, db
from models import Entry, User

import sqlalchemy
from sqlalchemy.orm import sessionmaker

def connect_with_sqlalchemy():
    creation_string = "%s+%s://%s:%s@%s/%s" % ("postgresql", "psycopg2", app.config['DATABASE_USER'], app.config['DATABASE_PASSWORD'], "localhost", app.config['DATABASE_NAME'])
    engine = sqlalchemy.create_engine(creation_string)
    Session = sessionmaker(bind=engine)
    return Session()

@app.before_request
def before_request():
    pass

@app.teardown_request
def after_request(response):
    pass

@app.route('/')
def show_entries():
    entries = Entry.query.all()
    return render_template("show_entries.html", entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(title=request.form['title'], text=request.form['text'])
    db.session.add(entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = User.query.filter_by(username=username, password=password).first()
        if not result:
            error = "Username and password do not match"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('You are registered')
        return redirect(url_for('login'))
    return render_template('register.html')
