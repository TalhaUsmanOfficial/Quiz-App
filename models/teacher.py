"""
! Created On Sun December 29 10:50 PM 2024

! @author: Talha Usman
! Status: Developer
"""

from models import db, check_password_hash, generate_password_hash
from .role import Role
from datetime import datetime


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    user_name = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(40), nullable=True)
    teacher_info = db.Column(db.Text, nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.Enum("Pending", "Approved", "Rejected", name="request_status"),
        nullable=False,
        default="Pending",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role_id = db.Column(
        db.Integer,
        db.ForeignKey("role.id", name="fk_user_role_id_role"),
        nullable=False,
    )   
    role = db.relationship("Role", backref=db.backref("teachers", lazy=True))
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", name="fk_user_category_id_category"),
        nullable=True,
    )
    category = db.relationship("Category", backref=db.backref("teachers", lazy=True))

    def __repr__(self):
        return f"Teacher(full_name='{self.full_name}', user_name='{self.user_name}')"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
