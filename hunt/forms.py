#coding=utf-8


from flaskext.wtf import Form, TextField, SubmitField, PasswordField, RadioField, \
     SelectMultipleField, SelectField, HiddenField, DateField, IntegerField, \
     validators, required, equal_to, email



class LoginForm(Form):
    email = TextField(u'登录邮箱', validators=[required(message=u'必填'),
                                               email(message=u'不是有效的邮箱地址') ])
    password = PasswordField(u'密码', validators=[required(message=u'必填')])
    next = HiddenField()


class RegisterForm(Form):
    email = TextField(u'登录邮箱', validators=[required(message=u'必填'),
                                               email(message=u'不是有效的邮箱地址') ])
    password = PasswordField(u'密码', validators=[required(message=u'必填')])
    confirm_password = PasswordField(u'确认密码', validators=[equal_to('password', message=u'密码不一致'),
                                                              required(message=u'必填')])

    agree_term = TextField(u'条款确认', validators=[required(message=u'必选')])
    # agree_term = SelectMultipleField(u'条款确认', validators=[required(message=u'必选')])


#### User profile edit ####
class GeneralInfoForm(Form):
    realname = TextField(u'姓名', validators=[required(message=u'必填')])
    sex = HiddenField(u'性别', validators=[required(message=u'必选')]) #, value='1')
    birthday = HiddenField(validators=[required(message=u'必填')]) #, value='1990-10-21')
    current_address = HiddenField(u'当前居住地址', validators=[required(message=u'必填')]) #, value='浙江,杭州')
    account_address = HiddenField(u'户口所在地址', validators=[required(message=u'必填')]) #, value='浙江,台州')
    phone_num = IntegerField(u'', validators=[required(message=u'必填')])
    

class EducationForm(Form):
    degree = TextField(u'学历', validators=[required(message=u'必填')])
    study_date = HiddenField(validators=[required(message=u'必填')])
    school = TextField(u'学校', validators=[required(message=u'必填')])
    speciality_type = HiddenField(u'专业类别', validators=[required(message=u'必填')])
    speciality = TextField(u'专业名称')
    
    

class ItSkillForm(Form):
    it_skills = HiddenField(u'IT技能', validators=[required(message=u'必填')])


#### [end] User profile edit #### 
