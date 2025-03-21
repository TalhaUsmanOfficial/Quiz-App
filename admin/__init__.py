"""
! Created On Sun December 22 12:40 AM 2024

! @author: Talha Usman
! Status: Developer
"""

from flask import Blueprint, session, render_template, redirect, url_for, request, flash
from models import db, Admin, User, Quiz, Category, Result, Role, Teacher, Review
from sqlalchemy import or_, and_, func, exists
from functools import wraps
from sqlalchemy.orm import aliased
from datetime import datetime
from variables import *

admin = Blueprint("admin", __name__)

from . import routes
