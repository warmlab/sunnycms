from flask import Blueprint

appraisal = Blueprint('appraisal', __name__)
from . import views
