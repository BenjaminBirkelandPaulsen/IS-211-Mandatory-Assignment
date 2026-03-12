from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"])
def list_users():
    """Return a list of all registered users."""
    users = User.query.all()
    return jsonify(
        [
            {"id": u.id, "name": u.name, "email": u.email, "phone": u.phone}
            for u in users
        ]
    )


@users_bp.route("/", methods=["POST"])
def create_user():
    """Register a new user."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip() or None

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(name=name, email=email, phone=phone)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Return details for a specific user."""
    user = db.get_or_404(User, user_id)
    return jsonify(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
        }
    )


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user."""
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
