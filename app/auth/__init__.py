from flask import Blueprint

# Create auth blueprint
auth = Blueprint('auth', __name__)

# Associate all views in auth with auth blueprint
from . import views