#!/usr/bin/env python
#coding=utf-8

import hashlib, urllib2, time, re
from datetime import datetime
from pyquery import PyQuery as pq
from models import db, Occupational, Job, Company


def get_headers(gzip=False):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13",
        # "User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-cn,zh;q=0.5",
        # "Accept-Encoding":"gzip,deflate",
        "Accept-Charset":"utf-8;q=0.7,*;q=0.7",
        "Keep-Alive":"115",
        "Connection":"keep-alive",
        # "Host":"",
        # "Referer":"",
    }
    if gzip:
        headers["Accept-Encoding"] = "gzip,deflate"
    return headers


def getDomFromUrl(url):
    req = urllib2.Request(
        url = url,
        headers = get_headers())
    try:
        request = urllib2.urlopen(req)
        source = request.read()
        request.close()
    except Exception, e:
        source = None
        print e

    ucontent = source.decode('utf-8')
    dom = pq(ucontent)
    return dom

def getCompanyInfo(dom):
    '''获取一个公司的信息'''
    info_items = dom('.companyInfoItems')
    info_trs = info_items('.companyInfoTab tr')
    

    company_info = {}
    for tr in info_trs:
        tr = pq(tr)
        k = tr('td:eq(0)').text().split(u'：')[0]
        v = tr('td:eq(1)').text()
        company_info[k] = v

    scale = company_info.get(u'公司规模')
    if scale:
        sh = re.search(r'(\d+)-(\d+)', scale)
        scale = sh.groups() if sh else (None, None)
    else:
        scale = (None, None)

    ####
    jcs = dom('.jobContact>div>div').find('div') # Job Contact
    for jc in jcs:
        jc = pq(jc)
        jctext = jc.text().split(u'：')
        if len(jctext) == 2:
            k, v = jctext
            company_info[k] = v 

    com = Company()
    com.name = info_items('.companyTitle').text()
    com.industry = company_info.get(u'公司行业')
    com.type = company_info.get(u'公司类型')
    com.address = company_info.get(u'公司地址')
    com.website = company_info.get(u'公司主页')
    com.scale_low, com.scale_high = scale
    com.email = None
    com.phone_num = None
    com.description = dom('.black12 tr:eq(2)').find('td').html()
    com.etag = ''

    return com




def getJobInfo(dom, company):
    '''获取一个职位的招聘信息'''

    job_info = {}
    type_tr = dom('.jobInfoItems tr:eq(0)')
    trtext = type_tr.text()
    trtext = trtext.split(u'：') if trtext else []
    if len(trtext) == 2:
        k, v = trtext
        v = v.replace('/', ',')
        job_info[k] = v

    trs = dom('.jobInfoItems tr:gt(1)')
    for tr in trs:
        tr = pq(tr)
        tds = tr('td')
        for td in tds:
            td = pq(td)
            tdtext = td.text().split(u'：')
            if len(tdtext) == 2:
                k, v = tdtext
                job_info[k] = v
    
    salary = job_info.get(u'职位月薪')
    if salary:
        sh = re.search(r'(\d+)-(\d+)', salary)
        salary = sh.groups() if sh else (None, None)
    else:
        salary = (None, None)
    quantity = job_info.get(u'招聘人数')
    if quantity:
        sh = re.search(r'(\d+)', quantity)
        quantity = sh.group(0) if sh else None

    job = Job()
    occ_type = job_info.get(u'职位类别')
    occ = Occupational.query.filter(Occupational.type==occ_type).first()
    if not occ:
        occ = Occupational()
        occ.name = 'FILL'
        occ.type = occ_type
        db.session.add(occ)
    job.occupational = occ
    job.type = job_info.get(u'工作性质')
    job.exp = job_info.get(u'工作经验')
    job.manage_exp = job_info.get(u'管理经验')
    job.quantity = quantity
    job.degree = job_info.get(u'最低学历')
    job.salary_low, job.salary_high = salary
    job.description = dom('.jobDes').html()
    job.etag = ''

    return job


def getPage(page_num):
    time.sleep(0.6)
    dom = getDomFromUrl('http://sou.zhaopin.com/jobs/jobsearch_jobtype.aspx?bj=160000&sj=045%3B079&jl=%E6%9D%AD%E5%B7%9E&sb=1&sm=0&p=' + page_num)
    table = dom('#contentbox table:eq(1)')
    trs = table('tr:gt(0)')

    iseven = True
    for tr in trs:
        if iseven:
            tr = pq(tr)
            job_title = tr('#dvJobTit').text()
            job_url = tr('#dvJobTit a').attr('href')
            company_name = tr('#dvCompNM').text()
            company_url = tr('#dvCompNM a').attr('href')
            work_place = tr('td:eq(4)').text().split(' - ')
            work_city = work_place[0]
            work_area = work_place[1] if len(work_place) > 1 else None
            public_date = tr('td:eq(5)').text()

            time.sleep(0.6)
            job_detail_dom = getDomFromUrl(job_url)
            
            company = getCompanyInfo(job_detail_dom)
            company.zhaopin_url = company_url
            db.session.add(company)
            
            job = getJobInfo(job_detail_dom, company)
            job.company = company
            job.title = job_title
            job.work_city = work_city
            job.work_area = work_area
            job.public_date = public_date
            job.zhaopin_url = job_url
            db.session.add(job)

            db.session.commit()
            print datetime.now()
            print 'This is Job %d' % job.id
            
        iseven = not iseven

    total_page = dom('.pagehead .num:eq(1)').text()
    sh = re.search(r'(\d+)/(\d+)', total_page)
    current_page, total_page = sh.groups() if sh else (None, None)
    return int(current_page), int(total_page)


def doSpider():
    print datetime.now()
    print 'Start Get First page'
    current_page, total_page = getPage('1')
    print 'First page, Done!'
    print 'Total page: %d\n' % total_page

    for page_num in range(current_page+1, total_page+1):
        print datetime.now()
        print 'Start get page: [%d]' % page_num
        getPage(str(page_num))
        print 'page: [%d], Done!\n' % page_num


if __name__ == '__main__':
    print 'BEGIN TEST'
    doSpider()
    print 'TEST DONE'
