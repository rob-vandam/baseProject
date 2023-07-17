from fastapi import Depends, FastAPI, HTTPException, Response, status, Request, Form
from fastapi.responses import StreamingResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union
from sqlalchemy.orm import Session
from typing import List
from .models import Users
from .schemas import User
from .database import session, engine,Base
import requests
import json
import pandas as pd
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = session() 
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_model=User)
async def root(action:str, admin_id:int, chain_id: int, app_id: int,lang:str, authtoken:Union[str, None] = None, db : Session = Depends(get_db)):
#    if action == 'open':
#       return Response(status_code=status.HTTP_200_OK)
    if action == 'uninstall':
         db_user = db.query(Users).filter(Users.app_id == app_id).first()
         db.delete(db_user)
         return Response(status_code=status.HTTP_200_OK)
    data = {'auth_token': authtoken}
    url = 'https://api.camping.care/v21/oauth/token'
    response = requests.request('POST', url, json=data)
    data = json.loads(response.text)
    refreshtoken = data['refreshToken']
    idtoken = data['idToken'] 
    db_user = db.query(Users).filter(Users.app_id == app_id).first()
    if db_user:
        if authtoken != db_user.authtoken or refreshtoken != db_user.refreshtoken or idtoken != db_user.idtoken:
            db_user.authtoken = authtoken
            db_user.refreshtoken = refreshtoken
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return Response(status_code=status.HTTP_200_OK)
        raise HTTPException(status_code=400, detail="User already registered")
    bk=Users(authtoken=authtoken,refreshtoken=refreshtoken,action=action,admin_id=admin_id, chain_id=chain_id,app_id=app_id,lang=lang)
    db.add(bk)
    db.commit()
    db.refresh(bk)
    return Response(status_code=status.HTTP_200_OK)

@app.get("/get_csv",response_class=HTMLResponse)
async def get_csv(request: Request, admin_id: int):
    return templates.TemplateResponse("select.html", {"request": request, "admin_id": admin_id})

@app.post("/get_csv")
async def get_csv(request: Request, admin_id:int=Form('admin_id'), status:str=Form('status'),accommodation:str=Form('accommodation'),payment:str=Form('payment'),db : Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.admin_id == admin_id).first()
    if db_user:
        data = {'refresh_token':db_user.refreshtoken}
        url = 'https://api.camping.care/v21/oauth/refresh_token'
        response = requests.request('POST', url, json=data)
        data = json.loads(response.text)
        refreshtoken = data['refresh_token']
        idtoken = data['id_token']       
        accesstoken = data['access_token']
        db_user.authtoken = accesstoken
        db_user.refreshtoken = refreshtoken
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        idToken = idtoken
        data = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(idToken),
        'x-admin-id': str(db_user.admin_id),
        }
        url = 'https://api.camping.care/v21/reservations'
        response = requests.request('GET', url, headers=data)
        data = json.loads(response.text)
        njson = []
        #print('data',data)
        for i in data:
            dict = {'id': i['id']}
            if status =='on':
                dict['status']=i['status']
            if accommodation =='on':
                dict['accommodation']=i['accommodation']['name']
            if payment == 'on':
                dict['payment']=i['payment']
            njson.append(dict)
        df = pd.read_json(json.dumps(njson))
        stream = io.StringIO()
        df.to_csv(stream, index=False, sep=';')
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    raise HTTPException(status_code=404, detail="Not found")
