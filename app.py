from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2:///json_sql"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return "Hello World!"


def create_models():
    from models import Record
    db.create_all()

if __name__ == '__main__':
    app.run(port=12248)

