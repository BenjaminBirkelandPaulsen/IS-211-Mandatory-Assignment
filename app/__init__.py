import os

from flask import Flask
from .extensions import db


def create_app(config=None):
    """Application factory for the BUA web application."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///bua.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    from .routes.home import home_bp
    from .routes.users import users_bp
    from .routes.items import items_bp
    from .routes.loans import loans_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(loans_bp)

    with app.app_context():
        db.create_all()

    return app
