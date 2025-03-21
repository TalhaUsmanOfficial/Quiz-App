"""
! Created On Sat December 21 11:01 PM 2024

! @author: Talha Usman
! Status: Developer
"""

from models import db, check_password_hash, generate_password_hash
from .role import Role


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Renamed 'results' backref to avoid conflict
    results = db.relationship(
        "Result", backref="owner", lazy=True, cascade="all, delete-orphan"
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey("role.id", name="fk_user_role_id_role"),
        nullable=True,
    )
    role = db.relationship("Role", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"{self.username}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
