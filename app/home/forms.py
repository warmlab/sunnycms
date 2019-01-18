from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("请输入标题", validators=[DataRequired()])
    summary = StringField("请输入摘要", validators=[DataRequired()])
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])

    submit = SubmitField('提交')
