from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Item

items_bp = Blueprint("items", __name__, url_prefix="/items")


@items_bp.route("/", methods=["GET"])
def list_items():
    """Return a list of all equipment items."""
    available_only = request.args.get("available", "").lower() == "true"
    query = Item.query
    if available_only:
        query = query.filter_by(available=True)
    items = query.all()
    return jsonify(
        [
            {
                "id": i.id,
                "name": i.name,
                "description": i.description,
                "category": i.category,
                "available": i.available,
            }
            for i in items
        ]
    )


@items_bp.route("/", methods=["POST"])
def create_item():
    """Add a new equipment item."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    item = Item(
        name=name,
        description=data.get("description", "").strip() or None,
        category=data.get("category", "").strip() or None,
    )
    db.session.add(item)
    db.session.commit()
    return (
        jsonify(
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "available": item.available,
            }
        ),
        201,
    )


@items_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Return details for a specific item."""
    item = db.get_or_404(Item, item_id)
    return jsonify(
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "category": item.category,
            "available": item.available,
        }
    )


@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """Update an equipment item."""
    item = db.get_or_404(Item, item_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        item.name = data["name"].strip()
    if "description" in data:
        item.description = data["description"].strip() or None
    if "category" in data:
        item.category = data["category"].strip() or None

    db.session.commit()
    return jsonify(
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "category": item.category,
            "available": item.available,
        }
    )


@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an equipment item."""
    item = db.get_or_404(Item, item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204
