"""
! Created On Mon December 30 12:03 AM 2024

! @author: Talha Usman
! Status: Developer
"""

from flask import request, render_template, redirect, url_for, session, Blueprint, flash
from models import db, User, Role, Teacher, Category, Quiz, Result
from sqlalchemy import or_, and_, func

teacher = Blueprint("teacher", __name__)

from . import routes
