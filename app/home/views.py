from flask import render_template
from flask import request, abort

from . import home

from ..models import Corporation, Post, Job

def posts(post_type):
    corporation = Corporation.query.first_or_404() # TODO the first corporation record
    posts = Post.query.filter_by(type=post_type).order_by(Post.modify_time.desc()).all() # 按日期倒序
    return render_template('home/posts.html', corporation=corporation, posts=posts)

@home.route('/', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.modify_time.desc()).limit(3).all()
    corporation = Corporation.query.first_or_404() # TODO the first corporation record
    return render_template('home/index.html', corporation=corporation, posts=posts)

@home.route('/news', methods=['GET'])
def news():
    return posts(1) # 1 - 最新咨询

@home.route('/achievements', methods=['GET'])
def achievement():
    return posts(2) # 2 - 最新业绩

@home.route('/joinin', methods=['GET'])
def joinin():
    corporation = Corporation.query.first_or_404() # TODO the first corporation record
    jobs = Job.query.all()
    return render_template('home/joinin.html', jobs=jobs, corporation=corporation)

@home.route('/aboutme', methods=['GET'])
def aboutme():
    corporation = Corporation.query.first_or_404() # TODO the first corporation record
    return render_template('home/aboutme.html', corporation=corporation)

@home.route('/post', methods=['GET'])
def post():
    id = request.args.get('id')
    if not id:
        abort(400)

    corporation = Corporation.query.first_or_404() # TODO the first corporation record
    post = Post.query.get_or_404(id)
    return render_template('home/post.html', corporation=corporation, post=post)
