from flask import redirect, url_for, request, abort

from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import AdminIndexView

from flask_security import login_required, current_user

from wtforms.validators import required
from .forms import PostForm, JobForm
from .forms import CKTextAreaField

from ..models import db
from ..models import Corporation

class BaseModelView(ModelView):
    page_size = 50
    can_view_details = True
    #create_modal = False
    #edit_modal = True

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('auth.login', next=request.url))

    # just for flask-login
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        pass

class PostModelView(BaseModelView):
    extra_js = ['http://cdn.ckeditor.com/4.11.1/standard/ckeditor.js']
    form = PostForm

class a():
    column_exclude_list = ['index', 'slug']
    column_searchable_list = ['title', 'summary']
    column_filters = ['title']
    column_editable_list = ['title']

    form_choices = {
        'type': [(1, '咨询'), (2, '业绩')]
    }
    form_excluded_columns = ['index', 'author', 'corporation', 'slug', 'modify_time']
    form_args = {
        'title': {
            'label': '标题',
            'validators': [required()]
        },
        'type': {
            'label': '类型',
            'validators': []
        },
        'summary': {
            'label': '摘要',
            'validators': [required()]
        },
        'body': {
            'label': '详细内容',
            'validators': [required()]
        },
        'publish_time': {
            'label': '发布时间'
        }
    }
    form_overrides = {
        'body': CKTextAreaField
    }

class JobModelView(BaseModelView):
    extra_js = ['http://cdn.ckeditor.com/4.11.1/standard/ckeditor.js']
    page_size = 50
    form = JobForm

class HomeView(AdminIndexView):
    @expose('/')
    def index(self):
        corporation = Corporation.query.first_or_404()
        return self.render('admin/index.html', corporation=corporation)

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('auth.login', next=request.url))
