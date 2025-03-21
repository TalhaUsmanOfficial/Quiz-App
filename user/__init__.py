"""
! Created On Fri January 03 10:23 PM 2025

! @author: Talha Usman
! Status: Developer
"""

from flask import (
    request,
    render_template,
    redirect,
    url_for,
    session,
    Blueprint,
    flash,
    jsonify,
)
from models import db, User, Role, Teacher, Category, Quiz, Result, Review
from functools import wraps
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased
from sqlalchemy import text
from variables import *
import uuid

user = Blueprint("user", __name__)

from . import routes
