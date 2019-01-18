from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):
    email = StringField('电子邮件', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')

    submit = SubmitField('登录')

    def validate_on_submit(self):
        return True
