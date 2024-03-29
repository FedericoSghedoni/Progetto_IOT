from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)

def register_blueprints(app):
    for module_name in ('home',):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

    # Impostiamo la pagina iniziale
    @app.route('/')
    def home():
        return render_template('home/start.html')


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
