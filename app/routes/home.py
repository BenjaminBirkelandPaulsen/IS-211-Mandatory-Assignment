from flask import Blueprint, render_template


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    """Render a simple landing page for the BUA service."""
    endpoints = [
        {
            "name": "Users",
            "path": "/users/",
            "web_path": "/users/page",
            "description": "Browse and register BUA members.",
        },
        {
            "name": "Items",
            "path": "/items/",
            "web_path": "/items/page",
            "description": "See equipment available for lending.",
        },
        {
            "name": "Loans",
            "path": "/loans/",
            "web_path": "/loans/page",
            "description": "Track active and returned loans.",
        },
    ]
    return render_template("home.html", endpoints=endpoints)