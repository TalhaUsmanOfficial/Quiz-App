"""
! Created On Wed December 25 1:16 AM 2024

! @author: Talha Usman
! Status: Developer
"""

from models import db
from variables import *


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_type = db.Column(db.JSON, nullable=True, default=lambda: [simple])
    description = db.Column(db.Text)
    total_rating = db.Column(db.Float, nullable=True, default=0)  # sum of all rating
    len_rating = db.Column(
        db.Float, nullable=True, default=0.0
    )  # number of users whom rated
    rating = db.Column(
        db.Float, nullable=True, default=0
    )  # total rating by calculating the average
    lock_rating = db.Column(db.Boolean, default=False, nullable=True)
    reviews = db.relationship("Review", backref="category", lazy=True)

    def __repr__(self):
        return f"Id: {self.id} Name: {self.name} Description: {self.description}"

    def calculate_rating(self):
        if not self.lock_rating:
            if self.len_rating > 0:
                if self.total_rating < 0:
                    self.total_rating *= -1
                self.rating = self.total_rating / self.len_rating
                self.rating = int(self.rating * 10) / 10
                db.session.commit()
