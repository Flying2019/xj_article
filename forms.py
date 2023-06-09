from wtforms import SubmitField,StringField,SelectMultipleField,RadioField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm

class GetRequire(FlaskForm):
    对立关键词1 = StringField(
        label="关键词1：",
        validators=[Length(2,2,message='关键词长度必须为2')],
        render_kw={
            "class": "form-control"
        },
    )
    定义关键词1 = StringField(
        label="定义关键词1：",
        validators=[],
        render_kw={
            "class": "form-control",
            'placeholder': u'[对立关键词1]'
        },
    )
    标签1 = SelectMultipleField(
        label="标签1：",
        validators=[],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control"
        },
        default=[]
    )
    对立关键词2 = StringField(
        label="关键词2：",
        validators=[Length(2,2,message='关键词长度必须为2')],
        render_kw={
            "class": "form-control"
        },
    )
    定义关键词2 = StringField(
        label="定义关键词1：",
        validators=[],
        render_kw={
            "class": "form-control",
            'placeholder': u'[对立关键词2]'
        },
    )
    标签2 = SelectMultipleField(
        label="标签2：",
        validators=[],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control"
        },
        default=[]
    )
    submit = SubmitField(u'提交')

class AddNormal(FlaskForm):
    type = SelectMultipleField(
        label="类型：",
        validators=[
            DataRequired("至少选择一项")
        ],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control"
        },
        default=[]
    )
    text = StringField(
        label=u'文本内容:',
        validators=[DataRequired(message='文本不能为空')],
        default=""
    )
    tag = SelectMultipleField(
        label="标签：",
        validators=[],
        coerce=int,
        choices=[],
        render_kw={
            "class": "form-control"
        },
        default=[]
    )
    submit = SubmitField(u'提交')
    
class AddType(FlaskForm):
    text = StringField(
        label=u'文本:',
        validators=[DataRequired(message='文本不能为空')],
    )
    type = RadioField(
        choices=[(0,'类型（无标签）'),(1,'类型（有标签）'),(2,'标签')],
        validators=[DataRequired(message='选1项')],
    )
    submit = SubmitField(u'添加')
    
class AddQry(FlaskForm):
    text = StringField(
        label=u'文本:',
        validators=[DataRequired(message='文本不能为空')],
    )
    submit = SubmitField(u'添加')