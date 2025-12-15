from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except:
    pass

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    if app.config.get("TESTING"):
        app.config["WTF_CSRF_ENABLED"] = False

    db.init_app(app)

    csrf.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
