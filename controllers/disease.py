def index():    
    result = db(db.diseases).select()
    return locals()

def create():
  # if session.status=="" or session.status==None:
  #   redirect(URL(c='login',f='index')) 

  # if session.emp_role in ['management','unit_management']:
  #   return "Access Denied"
  result = db(db.diseases).select(db.diseases.disease_code).last()
  if result is not None:
      disease_code = int(result.disease_code)+1
  else:
      disease_code = '1001' 
  disease_code=str(disease_code)
  return locals()

def add_validation(request):
  # validation
  errors =[]
  if not request.vars.disease_code:
      errors.append('SBU is required.')
  if not request.vars.disease_name:
      errors.append('Name is required.')

  # validation errors generate
  if errors:
      msg = ''
      for item in errors:
          msg = msg + item + ' <br>'
      session.flash = {"msg_type":"error","msg":msg}
      redirect (URL('disease','create'))
    # validation end
  return True
  
def submit():        
    disease_code = str(request.vars.disease_code)
    disease_name = str(request.vars.disease_name)
    
    validation=add_validation(request)    
    if validation==True:
      sql = """
          INSERT INTO diseases(disease_code, disease_name) 
          VALUES ('{disease_code}','{disease_name}')
          """.format(disease_code=disease_code,disease_name=disease_name)
      insert = db.executesql(sql)
      session.flash = {"msg_type":"success","msg":"Added successfully"}
      return  dict(redirect(URL('disease','index')))
    
def edit():
  if session.status=="" or session.status==None:
    redirect(URL(c='login',f='index'))
  if request.args(0):
      notices=db(db.notices.id==request.args(0)).select().first()
      return dict(notices=notices)
def update():
  if session.status=="" or session.status==None:
    redirect(URL(c='login',f='index'))
  notices=db(db.notices.id==request.args(0)).select().first()
  notices.update_record(
      notice_title = str(request.vars.notice_title),
      notice_desc = str(request.vars.notice_desc),
      publish_date = str(request.vars.publish_date) 
    )          
  return  dict(redirect(URL('notice','index')))  

## delete start##
def delete():
  if session.status=="" or session.status==None:
    redirect(URL(c='login',f='index'))
  if request.args(0):
      session.flash=T('Deleted Information')
      db(db.notices.id == request.args(0)).delete()
      return dict(redirect(URL('notice','index'))) 
## delete end##



def get_data():
  if session.status=="" or session.status==None:
    redirect(URL(c='login',f='index'))
      #Search Start##
  cid=str(session.cid)
  conditions = ""

  if  request.vars.notice_title != None and request.vars.notice_title !='':
      name = '%'+str(request.vars.notice_title)+'%'
      conditions = conditions +" and notice_title LIKE '"+name+"'"
  if  request.vars.date_from != None and request.vars.date_from != '':
      date = request.vars.date_from
      conditions = conditions +" and publish_date = '"+date+"'"
  if  request.vars.cid != None and request.vars.cid != '':
      cid = request.vars.cid
    #Search End## 

  ##Paginate Start##
  total_rows = len(db.executesql("SELECT * from notices WHERE notices.cid = '"+str(cid)+"' "+conditions, as_dict=True))
  page = int(request.vars.page or 1)
  rows_per_page = int(request.vars.rows_per_page or 10)
  if rows_per_page == -1:
          rows_per_page = total_rows
  start = (page - 1) * rows_per_page         
  end = start + rows_per_page
  ##Paginate End##

    ##Ordering Start##
  sort_column_index = int(request.vars['order[0][column]'] or 0)
  if sort_column_index == 0:
          sort_column_index = 1 #defult sorting column define
  sort_column_name = request.vars['columns[' + str(sort_column_index) + '][data]']
  sort_direction = request.vars['order[0][dir]']
    ##Ordering End##

    ##Querry Start##
  sql = """
  SELECT * from notices
  WHERE notices.cid = '"""+str(cid)+"""' 
  """+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
  """
  data = db.executesql(sql, as_dict=True)
    ##Qurry End##

  return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
            

  






