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
    status = str(request.vars.status)
    if status=='None':
      status=0
    
    validation=add_validation(request)    
    if validation==True:
      sql = """
          INSERT INTO diseases(disease_code, disease_name,status) 
          VALUES ('{disease_code}','{disease_name}','{status}')
          """.format(disease_code=disease_code,disease_name=disease_name,status=status)
      insert = db.executesql(sql)
      session.flash = {"msg_type":"success","msg":"Added successfully"}
      return  dict(redirect(URL('disease','index')))
    
def edit():
  # if session.status=="" or session.status==None:
  #   redirect(URL(c='login',f='index'))
  if request.args(0):
      disease=db(db.diseases.id==request.args(0)).select().first()
      return dict(disease=disease)
    
def update_validation(request,record):
  # validation
  errors =[]
  if not request.vars.disease_code:
      errors.append('Code is required.')
  if not request.vars.disease_name:
      errors.append('Name is required.')

  # validation errors generate
  if errors:
      msg = ''
      for item in errors:
          msg = msg + item + ' <br>'
      session.flash = {"msg_type":"error","msg":msg}
      redirect (URL('disease','edit',args=[record.id]))
    # validation end
  return True

def update():
  # if session.status=="" or session.status==None:
  #   redirect(URL(c='login',f='index'))
  if request.args(0):
    record=db(db.diseases.id==request.args(0)).select().first()
    validation=update_validation(request,record)
    status = str(request.vars.status)
    if status=='None':
      status=0
    if validation==True:
      record.update_record(
          disease_name = str(request.vars.disease_name),
          status = str(status) 
        )  
      session.flash = {"msg_type":"success","msg":"Update successfully"}        
      return  dict(redirect(URL('disease','index')))  

## delete start##
def delete():
  # if session.status=="" or session.status==None:
  #   redirect(URL(c='login',f='index'))
  if request.args(0):
      session.flash = {"msg_type":"warning","msg":"Deleted successfully"}        
      db(db.diseases.id == request.args(0)).delete()
      return dict(redirect(URL('disease','index'))) 
## delete end##







