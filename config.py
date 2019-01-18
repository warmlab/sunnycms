import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Sunny Admin <warmlab@outlook.com>'
    MAIL_SUBJECT_PREFIX = '[Muffins]'
    #BAKERY_ADMIN = os.environ.get('MUFFIN_ADMIN')
    #BAKERY_SLOW_DB_QUERY_TIME=0.5
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    UPLOAD_FOLDER = os.environ.get('SUNNYAPP_UPLOAD_DIR') or os.path.join(basedir, 'media')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DB_USER = os.environ.get('DB_USER') or 'nouser'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'nopassword'
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI =  'postgresql+psycopg2://%s:%s@127.0.0.1:5432/sunnyapp_dev' % (DB_USER, DB_PASSWORD)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DB_USER = os.environ.get('DB_USER') or 'nouser'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'nopassword'
    TESTING = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI =  'postgresql+psycopg2://%s:%s@127.0.0.1:5432/sunnyapp_test' % (DB_USER, DB_PASSWORD)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DB_USER = os.environ.get('DB_USER') or 'nouser'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'nopassword'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI =  'postgresql+psycopg2://%s:%s@127.0.0.1:5432/sunnyapp' % (DB_USER, DB_PASSWORD)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        #import logging
        #from logging.handlers import SMTPHandler
        #credentials = None
        #secure = None
        #if getattr(cls, 'MAIL_USERNAME', None) is not None:
        #    credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        #    if getattr(cls, 'MAIL_USE_TLS', None):
        #        secure = ()
        #mail_handler = SMTPHandler(
        #    mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        #    fromaddr=cls.MAIL_SENDER,
        #    toaddrs=[cls.ADMIN],
        #    subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
        #    credentials=credentials,
        #    secure=secure)
        #mail_handler.setLevel(logging.ERROR)
        #app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}
