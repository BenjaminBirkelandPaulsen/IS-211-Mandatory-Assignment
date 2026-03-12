from datetime import datetime, timezone

from .extensions import db


class User(db.Model):
    """A registered user of the BUA service."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    loans = db.relationship("Loan", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


class Item(db.Model):
    """An item of equipment available for loan through BUA."""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    loans = db.relationship("Loan", back_populates="item", lazy=True)

    def __repr__(self):
        return f"<Item {self.name}>"


class Loan(db.Model):
    """A record of an item being loaned to a user."""

    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    loaned_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    due_date = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="loans")
    item = db.relationship("Item", back_populates="loans")

    @property
    def is_active(self):
        return self.returned_at is None

    def __repr__(self):
        return f"<Loan user={self.user_id} item={self.item_id}>"
