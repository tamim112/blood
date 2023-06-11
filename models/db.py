# -- coding: utf-8 --

#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:d6160708-08e3-4217-bd9e-e9a550109a8d'   # before define_tables()
#auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
# Common Variable
#mreporting_http_pass='abC321'
# ' " / \ < > ( ) [ ] { } ,

#======================date========================
import datetime
import os

datetime_fixed=str(date_fixed)[0:19]    # default datetime 2012-07-01 11:48:10
current_date=str(date_fixed)[0:10]   # default date 2012-07-01

first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

#================blood_Database===================

#--------------------------- signature
signature=db.Table(db,'signature',
                Field('field1','string',length=100,default=''), 
                Field('field2','integer',default=0),
                Field('note','string',length=255,default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=session.user_id),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.user_id),
                )

#=====================User Setup================
db.define_table('users',
    Field("user_code",'string',length=10,requires=IS_NOT_EMPTY()),
    Field("first_name",'string',length=100,requires=IS_NOT_EMPTY()),
    Field("last_name",'string',length=100,requires=IS_NOT_EMPTY()),
    Field("full_name",'string',length=100,requires=IS_NOT_EMPTY()),
    Field("email",'string',length=50,requires=IS_NOT_EMPTY()),
    Field("password",'string',length=100,requires=IS_NOT_EMPTY()),
    Field('mobile', 'string',length=15),
    Field("date_of_birth",'date', requires=IS_NOT_EMPTY()),
    Field("gender",'string',requires=IS_NOT_EMPTY()),
    Field("age",'integer',requires=IS_NOT_EMPTY()),
    Field("weight",'integer'),
    Field("marital_status",'integer'),
    Field("university",'integer'),
    Field("country_code",'integer'),
    Field("district_code",'integer'),
    Field("city_code",'integer'),
    Field('address', 'string'),
    Field('blood_group', 'integer'),
    Field('occupation', 'integer'),
    Field('donation_status', 'integer'),
    Field('donation_date', 'date'),
    Field('diseases_status', 'integer'),
    Field('taken_status', 'string'),
    Field('thalassemia_status', 'integer'),
    Field('rank', 'integer'),
    Field('status', 'integer'),
    signature,
    migrate=False
)
#=====================Basic Setup================
db.define_table('diseases',
                Field("disease_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("disease_name",'string',length=100,requires=IS_NOT_EMPTY()),
                Field('status', 'integer',requires=IS_NOT_EMPTY),
                signature,
                migrate=False
            )

db.define_table('blood_groups',
                Field("group_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("group_name",'string',length=10,requires=IS_NOT_EMPTY()),
                Field('status', 'integer'),
                signature,
                migrate=False
            )

db.define_table('universities',
                Field("un_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("un_name",'string',length=100,requires=IS_NOT_EMPTY()),
                Field("country_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("district_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("city_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("location",'string',length=100),
                Field('status', 'integer'),
                signature,
                migrate=False
            )
db.define_table('occupations',
                Field("ocu_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("ocu_name",'string',length=100,requires=IS_NOT_EMPTY()),
                Field('status', 'integer'),
                signature,
                migrate=False
            )
db.define_table('countries',
                Field("country_code",'string',length=10,requires=IS_NOT_EMPTY()),
                Field("country_name",'string',length=100,requires=IS_NOT_EMPTY()),
                Field('status', 'integer'),
                signature,
                migrate=False
            )
db.define_table('districts',
            Field("district_code",'string',length=10,requires=IS_NOT_EMPTY()),
            Field("district_name",'string',length=100,requires=IS_NOT_EMPTY()),
            Field("country_code",'string',length=10,requires=IS_NOT_EMPTY()),
            Field('status', 'integer'),
            signature,
            migrate=False
        )
db.define_table('cities',
            Field("city_code",'string',length=10,requires=IS_NOT_EMPTY()),
            Field("city_name",'string',length=100,requires=IS_NOT_EMPTY()),
            Field("district_code",'string',length=10,requires=IS_NOT_EMPTY()),
            Field("country_code",'string',length=10,requires=IS_NOT_EMPTY()),
            Field('status', 'integer'),
            signature,
            migrate=False
        )

#=====================Basic Setup================

