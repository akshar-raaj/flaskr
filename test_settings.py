# configuration
DEBUG = True
TESTING = True
SECRET_KEY = 'development key'

DATABASE_NAME = 'flaskr_test'
DATABASE_USER = 'flaskr'
DATABASE_PASSWORD = 'abc'

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (DATABASE_USER, DATABASE_PASSWORD, 'localhost', DATABASE_NAME)
