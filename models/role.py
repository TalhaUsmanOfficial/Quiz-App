"""
! Created On Wed December 25 10:38 PM 2024

! @author: Talha Usman
! Status: Developer
"""

from . import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"Role: {self.name}"
