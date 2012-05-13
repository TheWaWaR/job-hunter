#coding=utf-8

import datetime
import json
from flask import Blueprint, request, session, render_template, url_for, abort, redirect
from hunt.extensions import db
from hunt.models import Job, Company, JobRequest

job = Blueprint('job', __name__)


@job.route('/search/')
@job.route('/search/p/<int:page>/')
def search(page=1):
    if page < 1 : page = 1

    exp = request.args.get('exp', '')
    salary = request.args.get('salary', 0, type=int)
    public_date = request.args.get('public_date', '')
    key_words = request.args.get('key_words' ,'')
    company_name = request.args.get('company_name' ,'')
    work_place = request.args.get('work_place' ,'')

    month_days = (31, 28, 31, 30, 31, 30,
                  31, 31, 30, 31, 30, 31)

    query = Job.query
    if exp and exp != u'不限':
        query = query.filter(Job.exp==exp)
    if salary:
        query = query.filter(Job.salary_low >= salary)
    if public_date and public_date != 'all':
        today = datetime.date.today()
        diff = datetime.timedelta(days=0)
        if public_date == 'month':
            last_month = today.month-2 if today.month>=2 else 11
            diff = datetime.timedelta(days=month_days[last_month])
        elif public_date == 'week':
            diff = datetime.timedelta(days=7)
        elif public_date == '3days':
            diff = datetime.timedelta(days=3)
        elif public_date == 'today':
            pass
        date_start = (today-diff).strftime('%Y-%m-%d')
        query = query.filter(Job.public_date >= date_start)

    if key_words:
        words = key_words.split()
        for word in words:
            query = query.filter(db.or_(Job.description.ilike('%'+ word +'%'),
                                        Job.title.ilike('%'+ word +'%')))
    if company_name:
        query = query.filter(Job.company.has(Company.name.ilike('%' + company_name + '%')))
    if work_place:
        place = work_place.split()
        if len(place) > 0:
            query = query.filter(Job.work_city==place[0])
            if len(place) == 2:
                query = query.filter(Job.work_area==place[1])

    page_url = lambda page: url_for('job.search', page=page,
                                    exp=exp, salary=salary,
                                    public_date=public_date, key_words=key_words,
                                    company_name=company_name, work_place=work_place)
    page_obj = query.paginate(page=page, per_page=20)

    return render_template('job-search.html',
                           page_obj=page_obj, page_url=page_url,
                           exp=exp, salary=salary,
                           public_date=public_date, key_words=key_words,
                           company_name=company_name, work_place=work_place)



@job.route('/view/<int:id>/')
def view(id):
    job = Job.query.get_or_404(id)
    return render_template('job-view.html', job=job)


@job.route('/addRequest/<int:job_id>/')
def addRequest(job_id):
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login',
                                next=url_for('job.addRequest', job_id=job_id)))

    job_request = JobRequest.query.filter(db.and_(JobRequest.user_id==uid,
                                                  JobRequest.job_id==job_id)).first()
    if job_request:
        return json.dumps({'success': False, 'message': u'已申请!'})
    else:
        job_request = JobRequest(user_id=uid, job_id=job_id)
        db.session.add(job_request)
        db.session.commit()
        return json.dumps({'success': True,
                           'from': 'add',
                           'url': url_for('job.delRequest', req_id=job_request.id)})


@job.route('/delRequest/<int:req_id>/')
def delRequest(req_id):
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login'))

    job_request = JobRequest.query.get_or_404(req_id)
    db.session.delete(job_request)
    db.session.commit()
    return json.dumps({'success': True,
                       'from': 'del',
                       'url': url_for('job.addRequest', job_id=job_request.job_id)})


@job.route('/feedback/')
@job.route('/feedback/<int:page>/')
def feedback(page=1):
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login',
                                next=url_for('job.feedback')))
    
    filter_ = request.args.get('filter', '') 
    if page < 1: page = 1
    cnt_total = JobRequest.query.filter(JobRequest.user_id==uid).count()
    cnt_feedbacked = JobRequest.query.filter(db.and_(JobRequest.user_id==uid,
                                                     JobRequest.feedbacked==True)).\
                                                     count()
    cnt_checked = JobRequest.query.filter(db.and_(JobRequest.user_id==uid,
                                                  JobRequest.checked==True)).\
                                                  count()
    query = JobRequest.query.filter(JobRequest.user_id==uid)
    if filter_:
        if filter_ == 'unfeedback':
            query = query.filter(JobRequest.feedbacked==False)
        else:
            query = query.filter(JobRequest.feedbacked==True)
            if filter_ == 'checked':
                query = query.filter(JobRequest.checked==True)
            elif filter_ == 'uncheck':
                query = query.filter(JobRequest.checked==False)

    query = query.order_by(JobRequest.createdate)

    page_url = lambda page: url_for('job.feedback',
                                    page=page,filter=filter_)
    page_obj = query.paginate(page=page, per_page=20)

    return render_template('job-feedback.html',
                           page_obj=page_obj, page_url=page_url,
                           cnt_total=cnt_total, cnt_feedbacked=cnt_feedbacked,
                           cnt_checked=cnt_checked, filter=filter_)


@job.route('/getFeedbackInfo/<int:req_id>/')
def getFeedbackInfo(req_id):
    uid = session.get('uid')
    if not uid:
        return redirect(url_for('account.login'))

    job_request = JobRequest.query.filter(db.and_(JobRequest.id==req_id,
                                                  JobRequest.user_id==uid)).first()
    if not job_request:
        return json.dumps({'success': False,
                           'message': u'此职位请求不存在或不为你所有.'})
    else:
        job_request.checked = True
        db.session.add(job_request)
        db.session.commit()
        return json.dumps({'success': True,
                           'hr_evaluate': job_request.hr_evaluate,
                           'hr_msg': job_request.hr_msg if job_request.hr_msg else ''})


@job.route('/recommend/')
def recommend():
    return render_template('job-recommend.html')

