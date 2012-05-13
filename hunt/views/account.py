#coding=utf-8

from datetime import datetime
import json

from flask import Blueprint, request, render_template, redirect, url_for, flash, \
     session
from sqlalchemy.exc import IntegrityError

from hunt.extensions import db
from hunt.forms import RegisterForm, LoginForm, GeneralInfoForm, EducationForm, ItSkillForm
from hunt.models import User


account = Blueprint('account', __name__)

#### Account ####
@account.route('/login/', methods=('GET', 'POST'))
def login():
    
    form = LoginForm(next=request.args.get('next', ''))
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter(db.and_(User.email==email,
                                             User.password==password)).first()
            if user:
                session['uid'] = user.id
                user.lastlogin = datetime.now()
                db.session.commit()
                next = form.next.data
                next = next if next else url_for('frontend.index')
                return redirect(next)
            else:
                flash(u'邮箱地址或密码错误!')
        else:
            print form.errors

    return render_template('login.html', form=form)


@account.route('/logout/')
def logout():
    if session.get('uid'):
        session.pop('uid')
    return redirect(url_for('frontend.index'))


@account.route('/register/', methods=('GET', 'POST'))
def register():

    form = RegisterForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            try:
                db.session.commit()
                return redirect(url_for('account.login'))
            except IntegrityError:
                db.session.rollback()
                flash(u'该邮箱已被注册!')
        else:
            print form.errors
    
    return render_template('register.html', form=form)



@account.route('/profile/edit/', methods=('GET', 'POST'))
def user_profile_edit():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login', next=url_for('account.user_profile_edit')))

    user = User.query.get(uid)
    gi_form = GeneralInfoForm()
    edu_form = EducationForm()
    itskill_form = ItSkillForm()

    return render_template('user-profile-edit.html', user=user,
                           gi_form=gi_form, edu_form=edu_form, itskill_form=itskill_form)



@account.route('/update/generalinfo/', methods=('POST',))
def update_general_info():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login', next=url_for('account.user_profile_edit')))

    form = GeneralInfoForm()

    user = User.query.get(uid)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success' : True, 'message' : u'更新成功!'})
    else:
        print form.errors
        form.errors['success'] = False
        form.errors['message'] = u'更新失败!'
        return json.dumps(form.errors)


@account.route('/update/educationinfo/', methods=('POST',))
def update_education_info():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login', next=url_for('account.user_profile_edit')))
    
    user = User.query.get(uid)
    form = EducationForm()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.study_start, user.study_end = form.study_date.data.split(',')
        # print user.study_start, user.study_end
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success' : True, 'message' : u'更新成功!'})
    else:
        print form.errors
        form.errors['success'] = False
        form.errors['message'] = u'更新失败!'
        return json.dumps(form.errors)

            

all_skills = ('Word', 'Excel', 'PowerPoint', 'C#', 'C',
              'C++', 'Java', 'JSP', 'PHP', 'VB',
              'VC++', 'SQLServer', 'Access', 'MySQL', 'Oracle',
              'SPSS', 'HTML', 'JavaScript', 'Linux', 'WINDOWS',
              '3DMAX', 'Flash', 'Premiere', 'Photoshop', 'CorelDraw',
              'Illustrator', 'AutoCAD', 'Pro/E', 'Protel', 'Python' ,
              'Emacs')

@account.route('/update/itskillinfo/', methods=('POST',))
def update_itskill_info():
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login',
                                next=url_for('account.user_profile_edit')))
    
    user = User.query.get(uid)
    form = ItSkillForm()
    if form.validate_on_submit():
        user.it_skills = form.it_skills.data
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success' : True, 'message' : u'更新成功!'})
    else:
        form.errors['success'] = False
        form.errors['message'] = u'更新失败!'
        return json.dumps(form.errors)
