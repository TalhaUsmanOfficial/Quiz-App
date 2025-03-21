"""
! Created On Sat December 21 10:31 PM 2024

! @author: Talha Usman
! Status: Developer
"""

# Sun 12 Jan 1:05 AM 2025

from flask import Flask, render_template, redirect, session, request, url_for
from models import db, Admin
from admin import admin
from user import user
from teacher import teacher
from auto_scripts import auto_script
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(teacher, url_prefix="/teacher")
app.register_blueprint(auto_script, url_prefix="/auto_script")
app.register_blueprint(user, url_prefix="/user")
app.secret_key = "12345"
migrate = Migrate(app, db)


@app.route("/")
def home():
    """
    Homepage of the website. Redirects to the user dashboard if the user is logged in.
    Otherwise, redirects to the user login page.
    """
    if "user_name" in session:
        return redirect(url_for("user.dashboard"))
    return redirect(url_for("user.login"))


# @app.route("/quiz")
# def quiz():
#     return redirect(url_for("auto_script.generate_quizzes"))


if __name__ == "__main__":
    # TODO: Create Admin Panel Manually for The First Time
    with app.app_context():
        # admin = Admin(username="username", email="myEmail@gmail.com")
        # admin.set_password("123")
        # db.session.add(admin)
        # db.session.commit()
        db.create_all()
    app.run(debug=True, port=8000)
    # TODO: .\myenv\Scripts\Activate.ps1

"""
Flask Migration:
if migrations directory not exists:
    flask db init
flask db migrate -m "Any Message"
flask db upgrade
"""
