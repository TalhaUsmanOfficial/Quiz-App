"""
! Created On Sat December 28 9:09 PM 2024

! @author: Talha Usman
! Status: Developer
"""

from flask import Blueprint, session, render_template, redirect, url_for, request
from models import db, Admin, User, Quiz, Category, Result, Role
from sqlalchemy import or_, and_, func
from datetime import datetime

auto_script = Blueprint("auto_script", __name__)

from . import generate_automated_data
