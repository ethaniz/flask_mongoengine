from flask import Flask
from views import bp
from config import Config
from models import db
from app.admin import create_admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    config = Config()

    app.config.from_object(config)

    bootstrap.init_app(app)

    init_login(app)

    register_blueprints(app)
    register_database(app)
    create_admin(app)

    return app

def register_blueprints(app):
    app.register_blueprint(bp)

def register_database(app):
    db.init_app(app)

def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.objects(id=user_id).first()
