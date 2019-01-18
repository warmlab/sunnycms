from flask import render_template, request, redirect, url_for

from flask_security import login_user

from . import auth
from .forms import LoginForm

from ..models import Corporation, Staff

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        print('877897899788989')
        if form.validate_on_submit():
            print('asklsakldklaslk')
            staff = Staff.query.filter_by(email=form.email.data).first()
            print('staff', staff)
            if staff and staff.verify_password(form.password.data):
                login_user(staff)
                return redirect(request.args.get('next') or url_for('home.index'))
        next = request.args.get('next') or url_for('home.index')
        return redirect(url_for('auth.login', next=next))
    else:
        corporation = Corporation.query.first_or_404() # TODO the first corporation record
        return render_template('auth/login.html', form=LoginForm(), corporation=corporation)
