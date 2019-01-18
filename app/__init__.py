from flask import Flask

from flask_mail import Mail
#from flask_login import LoginManager
from flask_security import Security

from config import config

from .models import db, staff_datastore
from .admin import init_admin

mail = Mail()
security = Security()
#loginManager = LoginManager()
#loginManager.session_protection = 'strong'
#loginManager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    security.init_app(app, staff_datastore)
    #loginManager.init_app(app)
    init_admin(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .appraisal import appraisal as app_blueprint
    app.register_blueprint(app_blueprint, url_prefix='/appraisal')

    return app
