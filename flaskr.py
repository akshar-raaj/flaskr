from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import psycopg2

app = Flask(__name__)
app.config.from_object('local_settings')

def connect_db():
    params = {}
    params['database'] = app.config['DATABASE_NAME']
    params['user'] = app.config['DATABASE_USER']
    params['password'] = app.config['DATABASE_PASSWORD']
    return psycopg2.connect(**params)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def after_request(response):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.cursor()
    cur.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("show_entries.html", entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    cur.execute('insert into entries (title, text) values(%s, %s)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = g.db.cursor()
        cur.execute("select * from users where username=%s and password=%s", [username, password])
        result = cur.fetchone()
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
        cur = g.db.cursor()
        cur.execute('insert into users(username, password) values(%s, %s)', [username, password])
        g.db.commit()
        flash('You are registered')
        return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
