from flask_admin import Admin

from .views import PostModelView, JobModelView
from .views import HomeView

from ..models import Post, Job
from ..models import db

def init_admin(app):
    admin = Admin(app, name='阳光评估', index_view=HomeView(name="首页"), template_mode='bootstrap3')
    admin.add_view(PostModelView(Post, db.session, name="业绩/咨询"))
    admin.add_view(JobModelView(Job, db.session, name="招聘职位"))
