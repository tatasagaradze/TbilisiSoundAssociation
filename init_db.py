from ext import app, db
import os
from models import *

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_user = User(username="admin", password="admin123", email="email", role="Admin")
    admin_user.create()