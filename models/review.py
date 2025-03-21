"""
! Created On Sun January 05 1:38 AM 2025

! @author: Talha Usman
! Status: Developer
"""

from models import db, Category


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", name="fk_user_id_review"), nullable=False
    )
    user = db.relationship("User", backref=db.backref("reviews", lazy=True))
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", name="fk_category_id_review"),
        nullable=False,
    )
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return f"Review(id={self.id}, user_id={self.user_id}, category_id={self.category_id}, rating={self.rating}, comment={self.comment})"
