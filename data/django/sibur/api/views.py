from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import datetime
import time
import hashlib
import json
from api.models import ReactorOne, Users


def index(request):
    df = pd.read_csv("frame_0.csv")

    reactor = ReactorOne()

    users = Users()

    ts = time.time()
    saltWord = 'ndssasdwq'

    if users.__class__.objects.all().count() == 0:
        users.__class__.objects.create(login = 'a431sw',passw = hashlib.sha256(('1234'+saltWord).encode('utf-8')).hexdigest(), role='0')
        users.__class__.objects.create(login = '1swb31',passw = hashlib.sha256(('4321'+saltWord).encode('utf-8')).hexdigest(), role='1')
    
    if reactor.__class__.objects.all().count() == 0:
        for i in range(df.shape[0]-1,-1,-1):
            reactor.__class__.objects.create(grate0_1 = df.iloc[i,0],
            grate0_2 = df.iloc[i,1],
            grate0_3 = df.iloc[i,2],
            grate0_4 = df.iloc[i,3],
            grate1_1 = df.iloc[i,4],
            grate1_2 = df.iloc[i,5],
            grate11_1 = df.iloc[i,6],
            grate11_2 = df.iloc[i,7],
            grate11_3 = df.iloc[i,8],
            grate11_4 = df.iloc[i,9],
            grate12_1 = df.iloc[i,10],
            grate12_2 = df.iloc[i,11],
            grate4_1 = df.iloc[i,12],
            grate4_2 = df.iloc[i,13],
            grate4_3 = df.iloc[i,14],
            grate4_4 = df.iloc[i,15],
            grate8_1 = df.iloc[i,16],
            grate8_2 = df.iloc[i,17],
            grate8_3 = df.iloc[i,18],
            grate8_4 = df.iloc[i,19],
            timestamp = datetime.datetime.fromtimestamp(ts-i*60).strftime('%Y-%m-%d %H:%M:%S'))
    
    req = {}

    if request.COOKIES.get('usco', None) == None:
        req['status'] = '403'
        
    else:
        req['status'] = '200'

    return HttpResponse(json.dumps(req))

def login(request):

    req = {}

    users = Users()

    if request.method == 'POST':
        user = users.__class__.objects.filter(login = request.POST['login'])

        if user.count() >= 1:

            if checkPass(user.values('passw'), request.POST['pass']):

                if user.values('role') == 0:
                    req['status'] = '200'
                    req['template'] = '<form action="http://localhost:8000/api/changeReactorState/?id=" method="POST"><button></button></form>'
                    return HttpResponse(json.dumps(req))

                else: 
                    req['status'] = '200'
                    return HttpResponse(json.dumps(req))

            else:
                req['status'] = '403'
                req['message'] = 'Вы ввели неверный пароль'
                return HttpResponse(json.dumps(req))

        else:
            req['status'] = '403'
            req['message'] = 'Вы попытались зайти под неверным пользователем'
            return HttpResponse(json.dumps(req))

    else:
        req['status'] = '403'
        return HttpResponse(json.dumps(req))


def checkPass(stored, provided):
    saltWord = 'ndssasdwq'
    return hashlib.sha256((provided+saltWord).encode('utf-8')).hexdigest() == stored
