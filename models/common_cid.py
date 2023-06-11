import datetime
import urllib
from gluon import DAL
db = DAL('mysql://root:@localhost/test_blood', decode_credentials=True)

date_fixed=datetime.datetime.now()+datetime.timedelta(hours=6)