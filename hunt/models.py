#coding=utf-8

from hunt.extensions import db
from datetime import datetime


class User(db.Model):
    """ 用户帐户 """
    __tablename__ = 'users'
    
    id                   = db.Column(db.Integer, primary_key=True)
    email                = db.Column(db.String(64), nullable=False, unique=True)
    password             = db.Column(db.String(64), nullable=False)
    phone_num            = db.Column(db.String(32))
    realname             = db.Column(db.String(32))  # 真实姓名
    degree               = db.Column(db.String(16))  # 学历
    school               = db.Column(db.String(64))  # 毕业学校
    speciality_type      = db.Column(db.String(64))  # 专业类别(第一级类别,第二级类别)
    speciality           = db.Column(db.String(32))  # 专业名称
    study_start          = db.Column(db.DateTime)    # 在上述学校起始就读时间
    study_end            = db.Column(db.DateTime)    # 毕业时间
    sex                  = db.Column(db.Boolean)     # 性别
    current_address      = db.Column(db.String(64))  # 当前所在地
    account_address      = db.Column(db.String(64))  # 户籍所在地
    birthday             = db.Column(db.DateTime)    # 生日
    it_skills            = db.Column(db.String(255)) # IT 技能列表 (存储 IT 技能列表中的 index)
    avatar_url           = db.Column(db.String(64))  # 头像图片存放的地址
    resume_url           = db.Column(db.String(64))  # 简历存放的地址
    expect_salary_low    = db.Column(db.Integer)     # 期望的最低薪水
    expect_salary_high   = db.Column(db.Integer)     # 期望的最高薪水
    lastlogin            = db.Column(db.DateTime)    # 上次登录的时间
    createdate           = db.Column(db.DateTime, default=datetime.now) # 注册时间



# class Industry(db.Model):
#     __tablename__ = 'industries'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column()


class Occupational(db.Model):           
    """ 职业 """
    __tablename__ = 'occupationals'
    
    id           = db.Column(db.Integer, primary_key=True)
    type         = db.Column(db.String(64))                 # 职业类别(格式: 类型1,类型2)
    name         = db.Column(db.String(32), nullable=False) # 职业名称


class Company(db.Model):
    """ 公司 """
    __tablename__ = 'companies'
    
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(32))
    industry     = db.Column(db.String(128)) # 所属的产业名称
    type         = db.Column(db.String(32))  # 类型(例如: 民营)
    scale_low    = db.Column(db.Integer)     # 规模
    scale_high   = db.Column(db.Integer)     # 规模
    address      = db.Column(db.String(255)) # 地址
    website      = db.Column(db.String(128)) # 网站地址
    email        = db.Column(db.String(64))
    phone_num    = db.Column(db.String(32))
    description  = db.Column(db.Text)        # 公司简介
    zhaopin_url  = db.Column(db.String(255)) # 该公司在 zhaopin.com 上的URL地址
    etag         = db.Column(db.String(128)) # 解决记录重复问题
    createdate   = db.Column(db.DateTime) # 记录创建时间


class Job(db.Model):
    """ 招聘信息 """
    __tablename__ = 'jobs'
    
    id                   = db.Column(db.Integer, primary_key=True)
    title                = db.Column(db.String(128)) # 招聘信息
    company_id           = db.Column(db.Integer, db.ForeignKey('companies.id')) # 发布的公司 ID
    occupational_id      = db.Column(db.Integer, db.ForeignKey('occupationals.id')) # 相应职业的 ID
    type                 = db.Column(db.String(32))  # 工作类型(例如:全职)
    work_city            = db.Column(db.String(255)) # 工作城市
    work_area            = db.Column(db.String(255)) # 工作城市的地区
    exp                  = db.Column(db.String(32))  # 最低工作经验要求
    manage_exp           = db.Column(db.String(32))  # 最低的管理经验要求
    quantity             = db.Column(db.Integer)     # 招聘人数
    degree               = db.Column(db.String(16))  # 最低学历要求
    salary_low           = db.Column(db.Integer)     # 薪水范围
    salary_high          = db.Column(db.Integer)     # 薪水范围
    description          = db.Column(db.Text)        # 职位描述/要求
    public_date          = db.Column(db.DateTime)    # 发布日期
    zhaopin_url          = db.Column(db.String(255)) # 该职位在 zhaopin.com 上的URL地址
    etag                 = db.Column(db.String(128)) # 解决记录重复问题
    createdate           = db.Column(db.DateTime, default=datetime.now) # 记录创建日期
    ## Relation
    company              = db.relation('Company')
    occupational         = db.relation('Occupational')



class JobRequest(db.Model):
    """ 求职申请 """
    __tablename__ = 'job_requests'
    
    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    job_id               = db.Column(db.Integer, db.ForeignKey('jobs.id')) # 对应的招聘信息 ID
    hr_evaluate          = db.Column(db.String(16))  # HR 对用户的评价
    hr_msg               = db.Column(db.String(255)) # HR 附带给用户的信息
    feedbackdate         = db.Column(db.DateTime)    # HR 反馈的时间
    feedbacked           = db.Column(db.Boolean, default=False) # HR 是否已反馈
    checked              = db.Column(db.Boolean, default=False) # HR 的反馈是否已被用户察看
    createdate           = db.Column(db.DateTime, default=datetime.now) # 申请的时间
    ## Relation
    user                 = db.relation('User')
    job                  = db.relation('Job')

    job_request_nix      = db.UniqueConstraint('user_id', 'job_id')


class JobRecommend(db.Model):
    __tablename__ = 'job_recommends'

    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    job_id               = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    checked              = db.Column(db.Boolean, default=False) # 是否已被用户察看
    ignored              = db.Column(db.Boolean, default=False) # 是否已被用户忽略
    createdate           = db.Column(db.DateTime, default=datetime.now)
    # Relation
    user                 = db.relation('User')
    job                  = db.relation('Job')



class Image(db.Model):
    """ 上传的图片 """
    __tablename__ = 'images'

    id                   = db.Column(db.Integer, primary_key=True)
    labelname            = db.Column(db.String(128)) # 前端显示的名字
    uploadname           = db.Column(db.String(128)) # 上传时的文件名
    savename             = db.Column(db.String(128)) # 存储在服务器的文件名

    user_id              = db.Column(db.Integer, db.ForeignKey('users.id'))
    user                 = db.relation('User', backref='images', uselist=False)



# class ZhaopinRecord(db.Model):
#     """存储从 zhaopin.com(智联招聘) 上抓取过来的职位信息"""
#     pass

