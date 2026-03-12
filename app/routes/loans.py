from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import Item, Loan, User

loans_bp = Blueprint("loans", __name__, url_prefix="/loans")


@loans_bp.route("/", methods=["GET"])
def list_loans():
    """Return all loans, optionally filtering to active loans only."""
    active_only = request.args.get("active", "").lower() == "true"
    loans = Loan.query.all()
    if active_only:
        loans = [loan for loan in loans if loan.is_active]
    return jsonify(
        [
            {
                "id": loan.id,
                "user_id": loan.user_id,
                "item_id": loan.item_id,
                "loaned_at": loan.loaned_at.isoformat(),
                "due_date": loan.due_date.isoformat() if loan.due_date else None,
                "returned_at": (
                    loan.returned_at.isoformat() if loan.returned_at else None
                ),
                "is_active": loan.is_active,
            }
            for loan in loans
        ]
    )


@loans_bp.route("/", methods=["POST"])
def create_loan():
    """Record a new loan of an item to a user."""
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    item_id = data.get("item_id")
    due_date_str = data.get("due_date")

    if not user_id or not item_id:
        return jsonify({"error": "user_id and item_id are required"}), 400

    _user = db.get_or_404(User, user_id)
    item = db.get_or_404(Item, item_id)

    if not item.available:
        return jsonify({"error": "item is not available for loan"}), 409

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            return jsonify({"error": "invalid due_date format, use ISO 8601"}), 400

    loan = Loan(user_id=user_id, item_id=item_id, due_date=due_date)
    item.available = False
    db.session.add(loan)
    db.session.commit()
    return (
        jsonify(
            {
                "id": loan.id,
                "user_id": loan.user_id,
                "item_id": loan.item_id,
                "loaned_at": loan.loaned_at.isoformat(),
                "due_date": loan.due_date.isoformat() if loan.due_date else None,
                "is_active": loan.is_active,
            }
        ),
        201,
    )


@loans_bp.route("/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    """Return details for a specific loan."""
    loan = db.get_or_404(Loan, loan_id)
    return jsonify(
        {
            "id": loan.id,
            "user_id": loan.user_id,
            "item_id": loan.item_id,
            "loaned_at": loan.loaned_at.isoformat(),
            "due_date": loan.due_date.isoformat() if loan.due_date else None,
            "returned_at": (
                loan.returned_at.isoformat() if loan.returned_at else None
            ),
            "is_active": loan.is_active,
        }
    )


@loans_bp.route("/<int:loan_id>/return", methods=["POST"])
def return_loan(loan_id):
    """Mark an item as returned."""
    loan = db.get_or_404(Loan, loan_id)

    if not loan.is_active:
        return jsonify({"error": "item has already been returned"}), 409

    loan.returned_at = datetime.now(timezone.utc)
    loan.item.available = True
    db.session.commit()
    return jsonify(
        {
            "id": loan.id,
            "user_id": loan.user_id,
            "item_id": loan.item_id,
            "returned_at": loan.returned_at.isoformat(),
            "is_active": loan.is_active,
        }
    )
