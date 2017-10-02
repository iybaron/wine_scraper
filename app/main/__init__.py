from flask import Blueprint

# Create main blueprint
main = Blueprint('main', __name__)

# Associate all views in main with main blueprint
from . import views