"""
! Created On Sat December 21 11:00 PM 2024

! @author: Talha Usman
! Status: Developer
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

from .user import *
from .quiz import *
from .admin import *
from .category import *
from .role import Role
from .teacher import Teacher
from .review import Review
