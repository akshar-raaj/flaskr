from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('local_settings')
c = app.config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s/%s' % (c['DATABASE_USER'], c['DATABASE_PASSWORD'], 'localhost', c['DATABASE_NAME'])

db = SQLAlchemy(app)
