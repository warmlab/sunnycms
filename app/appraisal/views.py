from flask import render_template

from . import appraisal

from ..models import Appraisal, Corporation

@appraisal.route('/', methods=['GET'])
def index():
    #apps = Appraisal.query.all()
    corporation = Corporation.query.first_or_404()
    return render_template('appraisal/index.html', corporation=corporation)
