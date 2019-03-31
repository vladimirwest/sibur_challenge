from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import glob
import numpy as np
from catboost import CatBoostClassifier
import datetime
import time
import hashlib
from django.views.decorators.csrf import csrf_exempt
import json
from api.models import ReactorOne, Users
from pandas.io.json import json_normalize

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
            timestamp = int(ts)-i*60)
    
    req = {}


    if request.COOKIES.get('usco', None) == None:
        req['status'] = '403'
        req['dataTemp'] = getBdData()
        return HttpResponse(json.dumps(req))

        
    else:
        req['status'] = '200'
        req['dataTemp'] = getBdData()
        return HttpResponse(json.dumps(req))
		
@csrf_exempt
def login(request):

    req = {}

    users = Users()

    if request.method == 'GET':
        user = users.__class__.objects.filter(login = request.POST['login'])

        if user.count() >= 1:

            if checkPass(user.values('passw'), request.POST['pass']):

                if user.values('role') == '0':
                    req['status'] = '200'
                    req['template'] = '<form action="http://localhost:8000/api/changeReactorState/?id=" method="POST"><button></button></form>'
                    resp = HttpResponse(json.dumps(req))
                    set_cookie(resp, 'usco', hashlib.sha256((request.POST['login']+user.values('login')).encode('utf-8')).hexdigest())
                    return HttpResponseRedirect('95.181.226.169')

                else: 
					
                    req['status'] = '200'
                    resp = HttpResponse(json.dumps(req))
                    set_cookie(resp, 'usco', hashlib.sha256((request.POST['login']+user.values('login')).encode('utf-8')).hexdigest())
                    return HttpResponseRedirect('95.181.226.169')

            else:
                req['status'] = '403'
                req['message'] = 'Вы ввели неверный пароль'
                return HttpResponseRedirect('95.181.226.169')

        else:
            req['status'] = '403'
            req['message'] = 'Вы попытались зайти под неверным пользователем'
            return HttpResponseRedirect('95.181.226.169')

    else:
        req['status'] = '403'
        return HttpResponseRedirect('95.181.226.169')


def checkPass(stored, provided):
    saltWord = 'ndssasdwq'
    return hashlib.sha256((provided+saltWord).encode('utf-8')).hexdigest() == stored
	
	
def set_cookie(response, key, value, days_expire = 7):
	if days_expire is None:
		max_age = 365 * 24 * 60 * 60  #one year
	else:
		max_age = days_expire * 24 * 60 * 60 
	expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
	response.set_cookie(key, value, max_age=max_age, expires=expires)


def jitter(d):
    """
    Calculate jitter.
    """

    return pd.Series(np.mean(np.abs(d.values[1:] - d.values[:-1]), axis=0),
                     index=["_".join([cl, "jitter"]) for cl in d.columns])


def get_trend(d):
    """
    Calcuate trend for a frame `d`.
    """

    dv = d.reset_index(drop=True)
    dv["minutes"] = np.arange(dv.shape[0], dtype=np.float64)
    covariance = dv.cov()
    return (((covariance["minutes"]) / covariance.loc["minutes", "minutes"])[d.columns]
            .rename(lambda cl: "_".join([cl, "trend"])))


def get_features(frame):
    """
    Calculate simple features for dataframe.
    """

    average_sensors = frame.mean(axis=1)
    average_temp = average_sensors.mean()
    std_temp = average_sensors.std()
    min_temp = average_sensors.min()
    max_temp = average_sensors.max()

    features = []
    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean"])))
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std"])))
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min"])))
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max"])))

    features.append(frame.mean().rename(lambda cl: "_".join([cl, "mean_norm"])) / average_temp)
    features.append(frame.std().rename(lambda cl: "_".join([cl, "std_norm"])) / std_temp)
    features.append(frame.min().rename(lambda cl: "_".join([cl, "min_norm"])) / min_temp)
    features.append(frame.max().rename(lambda cl: "_".join([cl, "max_norm"])) / max_temp)

    features.append(jitter(frame))
    features.append(get_trend(frame))
    features.append(jitter(frame).rename(lambda cl: "_".join([cl, "norm"])) / (max_temp - min_temp))

    features.append(average_sensors.apply(["mean", "std", "min", "max"]))
    return pd.concat(features)


def getPredictions(frame_data):
    text_file = open("SIM_COLS.txt", "r")
    lines = text_file.read().split('\n')
    SIM_COLS = lines[:-1]

    models_files = glob.glob("/home/eugenia/rcs/sibur/api/models/models/*")

    test_preds = pd.DataFrame()
    test_features = get_features(frame_data)
    test_features = pd.DataFrame(test_features)
    test_features = test_features.T
    for file_name in models_files:
        model = CatBoostClassifier()
        model.load_model(file_name)
        sensor = file_name[42:-4]
        local_preds = model.predict_proba(test_features[SIM_COLS].values)[:, 1]
        test_preds[sensor] = pd.Series(local_preds.astype(np.float), index=test_features.index)
    print(test_preds)

def getBdData(period = 60):
	reactor = ReactorOne()
	return reactor.__class__.objects.all().values()[:period][::-1]