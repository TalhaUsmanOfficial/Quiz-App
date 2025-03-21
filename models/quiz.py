"""
! Created On CURRENT_DAY December 21 CURRENT_HOUR_12:09 CURRENT_AMPM 2024

! @author: Talha Usman
! Status: Developer
"""

from models import db
from datetime import datetime
from .category import Category


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Text, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False, default=1
    )
    category = db.relationship("Category", backref=db.backref("quizzes", lazy=True))

    def __repr__(self):
        return f"Quiz(id={self.id}, question={self.question}, option1={self.option1}, option2={self.option2}, option3={self.option3}, option4={self.option4}, correct_option={self.correct_option})"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", name="fk_result_user_id"), nullable=False
    )
    user = db.relationship(
        "User", backref=db.backref("user_results", lazy=True)
    )  # Renamed backref
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id", name="fk_result_category_id"),
        nullable=True,
    )
    category = db.relationship("Category", backref=db.backref("results", lazy=True))
    score = db.Column(db.Integer, nullable=False)
    result_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Result(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score})"
