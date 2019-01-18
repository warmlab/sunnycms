from wtforms import Form, TextAreaField
from wtforms.widgets import TextArea
from wtforms.fields import StringField, RadioField, DateTimeField, TextAreaField, SelectField, IntegerField
from wtforms.validators import required

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] = ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class PostForm(Form):
    title = StringField('标题', validators=[required()])
    type = SelectField('类型', choices=[('1', '咨询'), ('2', '业绩')], default='1')
    summary = StringField('摘要', validators=[required()])
    body = CKTextAreaField('详细内容', validators=[required()])
    publish_time = DateTimeField('发布时间')

class JobForm(Form):
    name = StringField('职位名称', validators=[required()])
    #min_experience_yeas = IntegerField('最低工作经验（年）')
    max_age = IntegerField('最大年龄')
    salary_from = IntegerField('工资起始值')
    salary_to = IntegerField('工资最大值')
    duty = CKTextAreaField('工作职责', validators=[required()])
    summary = CKTextAreaField('工作描述', validators=[required()])
    skills = CKTextAreaField('所需技能', validators=[required()])
    publish_time = DateTimeField('发布时间')
