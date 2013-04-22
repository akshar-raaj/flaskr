from flask import Flask

app = Flask(__name__)
app.config.from_object('local_settings')

from views import *

if __name__ == '__main__':
    app.run()
